import sponsor_finder
import os
import requests

from alive_progress import alive_it
from termcolor import cprint


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def printTitle():
    TITLE = """
.▄▄ ·  ▄▄▄·       ▐ ▄ .▄▄ ·       ▄▄▄      ·▄▄▄▪   ▐ ▄ ·▄▄▄▄  ▄▄▄ .▄▄▄  
▐█ ▀. ▐█ ▄█▪     •█▌▐█▐█ ▀. ▪     ▀▄ █·    ▐▄▄·██ •█▌▐███▪ ██ ▀▄.▀·▀▄ █·
▄▀▀▀█▄ ██▀· ▄█▀▄ ▐█▐▐▌▄▀▀▀█▄ ▄█▀▄ ▐▀▀▄     ██▪ ▐█·▐█▐▐▌▐█· ▐█▌▐▀▀▪▄▐▀▀▄ 
▐█▄▪▐█▐█▪·•▐█▌.▐▌██▐█▌▐█▄▪▐█▐█▌.▐▌▐█•█▌    ██▌.▐█▌██▐█▌██. ██ ▐█▄▄▌▐█•█▌
 ▀▀▀▀ .▀    ▀█▄▀▪▀▀ █▪ ▀▀▀▀  ▀█▄▀▪.▀  ▀    ▀▀▀ ▀▀▀▀▀ █▪▀▀▀▀▀•  ▀▀▀ .▀  ▀
    """

    cprint(TITLE, "blue")
    cprint(" Created by: @b0kch01 for Hack@UCI ", "yellow", on_color="on_grey")
    print()


def getSessionID():
    if os.path.exists("session_id.txt"):
        with open("session_id.txt", "r") as f:
            return f.read()
    else:
        session_id = input("Session ID: ")
        with open("session_id.txt", "w") as f:
            f.write(session_id)

        return session_id


def main():
    clear()

    printTitle()

    session_id = getSessionID()

    company_chosen = input("Search company by name (blank to go back): ")

    while company_chosen != "":

        sf = sponsor_finder.SponsorFinder(
            session_id=session_id,
            company=company_chosen
        )

        print("\n------------------[ INFORMATION ]--------------------\n")

        sf.run()

        company = sf.companies_info[company_chosen]

        print(f"Name: {company.name}")
        print(f"Domain: {company.domain}")
        print(f"Employees: {company.size}")
        print(f"Type: {'Big Tech' if company.size > 10000 else 'Tech'}")

        print("\n-----------------[ TOP CANDIDATES ]------------------\n")

        sf.print_top_five(company_chosen)

        sf.get_email_for_top_person(company_chosen)
        sf.copy_spreadsheet_row(company_chosen)

        print()
        cprint("Row copied to clipboard!", "green")

        company_chosen = input("\nSearch company (empty to exit): ")


def simplify(raw_text):
    return "".join([c for c in raw_text.lower() if c.isalnum()])


def turboMode():
    clear()
    printTitle()

    try:
        with open("input/existing.txt", "r") as f:
            checked_companies = map(simplify, f.read().splitlines())

        with open("input/new.txt", "r") as f:
            new_companies = map(simplify, f.read().splitlines())
    except FileNotFoundError:
        helpMode()
        return

    # Get the non-intersection of the two lists
    new_companies = sorted(list(set(new_companies) - set(checked_companies)))

    if "y" != input(f"Found {len(new_companies)} new companies. Continue? [Y/n] ").lower():
        return

    clear()
    printTitle()

    print("Search has started!\n")

    session_id = getSessionID()

    sf = sponsor_finder.SponsorFinder(
        session_id=session_id,
        companies=new_companies
    )

    sf.run()

    purged = sf.purge_empty_companies()
    cprint(f"⏺ Purged {len(purged)} companies with no people", "yellow")

    try:
        for company, peoples in alive_it(sf.companies_people.items(), title="⏺ Fetching emails"):
            if len(peoples) > 0:
                sf.get_email_for_top_person(company)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            cprint("\nYou have ran out of tokens!", "red")
            cprint("Because results are cached based on authkey, a copy of the results have been copied to your clipboard.", "blue")
            cprint("Make sure you transfer the results to a spreadsheet before continuing.", "blue")

            input("\nPress [Enter] to continue... ")
            return

    sf.copy_spreadsheet_rows(sf.companies_people.keys())
    cprint("A copy of the results have been copied to your clipboard.", "blue")
    input("\nPress [Enter] to continue... ")


def helpMode():
    clear()

    cprint("Turbomode Checklist:\n", "blue")
    cprint(" 1. Place existing companies in input/existing.txt")

    try:
        with open("input/existing.txt", "r") as file:
            existing_count = len(file.readlines())

        cprint(f"    [✓] Found {existing_count} existing companies", "green")
    except FileNotFoundError:
        cprint(f"    [!] File not found in directory.", "yellow")

    cprint(" 2. Place new companies in input/new.txt")

    try:
        with open("input/new.txt", "r") as file:
            existing_count = len(file.readlines())

        cprint(f"    [✓] Found {existing_count} new companies", "green")
    except FileNotFoundError:
        cprint(f"    [!] File not found in directory.", "yellow")

    cprint(" 3. Select turbo mode in the main menu")
    cprint(" 4. Results will copied into the clipboard (paste into sponsorship tracker sheet)")

    input("\nPress [Enter] to return to the main menu.")


def main_menu():
    while True:
        clear()
        printTitle()

        print("1. Single Mode")
        print("2. Automatic Mode")
        print("3. Exit\n")

        while (choice := input("Enter option (? for help): ")) not in ["1", "2", "3", "?"]:
            clear()
            printTitle()

            print("1. Single Mode")
            print("2. Automatic Mode")
            print("3. Exit")

            cprint("\nInvalid, try again!", "red")

        if choice == "1":
            main()
        elif choice == "2":
            turboMode()
        elif choice == "?":
            helpMode()

        else:
            break


if __name__ == "__main__":
    try:
        main_menu()
    except (sponsor_finder.SponsorFinderException, AssertionError) as e:
        cprint(f"Error: {e}", "red")
