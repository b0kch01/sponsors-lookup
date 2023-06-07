import clearbit
import clipboard
import pandas as pd


class SponsorFinderException(Exception):
    pass


class SponsorFinder:

    @staticmethod
    def fuzzy_in(haystack, needles):
        for needle in needles:
            if needle.lower() in haystack.lower():
                return True
        return False

    def __init__(self, *, company=None, companies=None, session_id):
        self.companies_people = {k: [] for k in (companies or [company])}
        self.companies_info = {k: [] for k in (companies or [company])}
        self.session_id = session_id

    def calculate_points(self, person):
        score = 1000

        # technical evangelists or advocates
        if self.fuzzy_in(person['title'], ['evangelist', 'advocate']):
            score += 500

        # campus or university recruiters
        if self.fuzzy_in(person['title'], ['campus', 'university']):
            score += 100

        # recruiters
        if self.fuzzy_in(person['title'], ['recruiter', 'recruiting', 'talent', 'sourcing', 'sourcer']):
            score += 50

        # points for being technical
        if self.fuzzy_in(person['title'], ['technical']):
            score += 20

        # subtract points for being global or international
        if self.fuzzy_in(person['title'], ['global', 'international', 'worldwide']):
            score -= 10

        # subtract points for diversity and inclusion
        if self.fuzzy_in(person['title'], ['diversity', 'inclusion', "de&i", "dei", "d&i"]):
            score -= 20

        # subtract points for very high level titles
        if self.fuzzy_in(person['title'], ['senior', 'vp', 'director', 'head', 'lead', 'executive', 'chief', 'principal']):
            score -= 10

        # subtract points for very lower, but still senior titles
        if self.fuzzy_in(person['title'], ['manager', 'associate', 'assistant', 'coordinator', 'specialist']):
            score -= 5

        return score

    def run(self):
        for company in list(self.companies_people.keys()):
            self.fetch_company_and_people_info(company)

    def fetch_company_and_people_info(self, company_name):
        cbs = clearbit.ClearBitSession(session_id=self.session_id)

        company = cbs.get_top_company(company_name)
        people = cbs.get_people(company, clearbit.Role.RECRUITING)
        people += cbs.get_people(company, clearbit.Role.ENGINEERING)

        for person in people:
            person["quality_score"] = self.calculate_points(person)

        people.sort(key=lambda x: x['quality_score'], reverse=True)

        self.companies_info[company_name] = company
        self.companies_people[company_name] = people

    def get_email_for_top_person(self, company):
        if company not in self.companies_people or len(self.companies_people[company]) == 0:
            raise SponsorFinderException("No company or no people found for company")

        cbs = clearbit.ClearBitSession(session_id=self.session_id)
        self.companies_people[company][0]['email'] = cbs.get_person_info(
            self.companies_people[company][0]["id"])['email']

    def copy_spreadsheet_row(self, company_name: str):
        if (company_name not in self.companies_people or
                len(self.companies_people[company_name]) == 0):
            raise SponsorFinderException("No company or no people found for company")

        company = self.companies_info[company_name]
        top_person = self.companies_people[company_name][0]

        clipboard.copy(
            f"{company.name}\t"
            f"Tech\t{top_person['first_name']}\t{top_person['last_name']}\t"
            f"{top_person['email']}\t\t"
            f"Not Contacted Yet\t\t{top_person['title']}"
        )

    def print_top_five(self, company_name: str):
        if (company_name not in self.companies_people or
                len(self.companies_people[company_name]) == 0):
            return

        company = self.companies_info[company_name]
        people = self.companies_people[company_name]

        df = pd.DataFrame(people[:5])
        df = df[['first_name', 'last_name', 'title', 'quality_score']]
        print(df.to_markdown(index=False))
