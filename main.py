import sponsor_finder
import os
from termcolor import cprint


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear()

    TITLE = """
.▄▄ ·  ▄▄▄·       ▐ ▄ .▄▄ ·       ▄▄▄      ·▄▄▄▪   ▐ ▄ ·▄▄▄▄  ▄▄▄ .▄▄▄  
▐█ ▀. ▐█ ▄█▪     •█▌▐█▐█ ▀. ▪     ▀▄ █·    ▐▄▄·██ •█▌▐███▪ ██ ▀▄.▀·▀▄ █·
▄▀▀▀█▄ ██▀· ▄█▀▄ ▐█▐▐▌▄▀▀▀█▄ ▄█▀▄ ▐▀▀▄     ██▪ ▐█·▐█▐▐▌▐█· ▐█▌▐▀▀▪▄▐▀▀▄ 
▐█▄▪▐█▐█▪·•▐█▌.▐▌██▐█▌▐█▄▪▐█▐█▌.▐▌▐█•█▌    ██▌.▐█▌██▐█▌██. ██ ▐█▄▄▌▐█•█▌
 ▀▀▀▀ .▀    ▀█▄▀▪▀▀ █▪ ▀▀▀▀  ▀█▄▀▪.▀  ▀    ▀▀▀ ▀▀▀▀▀ █▪▀▀▀▀▀•  ▀▀▀ .▀  ▀
    """

    # 83ee5038418c5ed535ff0e5e5f7704b8e9561f9f86dd8563391aa220d341c0f1

    cprint(TITLE, "blue")
    print()

    if os.path.exists("session_id.txt"):
        with open("session_id.txt", "r") as f:
            session_id = f.read()
    else:
        session_id = input("Session ID: ")
        with open("session_id.txt", "w") as f:
            f.write(session_id)

    company_chosen = input("Search company: ")

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


if __name__ == "__main__":
    try:
        main()
    except (sponsor_finder.SponsorFinderException, AssertionError) as e:
        cprint(f"Error: {e}", "red")
