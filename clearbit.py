from dataclasses import dataclass

from path import Path
import requests


_API_BASE = Path('https://connect.clearbit.com/v1')
_AUTOCOMPLETE_BASE = Path('https://autocomplete.clearbit.com/v1')


class Role:
    RECRUITING = 'recruiting'
    PR = 'public_relations'
    SALES = 'sales'
    ENGINEERING = 'engineering'


@dataclass(frozen=True)
class Company:
    name: str
    domain: str


class ClearBitSession:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def get_top_company(self, query: str):
        companies = self.get_companies(query)
        top_company = companies[0]
        return Company(name=top_company['name'], domain=top_company['domain'])

    def get_companies(self, query: str):
        # Example: https://autocomplete.clearbit.com/v1/companies/suggest?query=google
        url = _AUTOCOMPLETE_BASE / 'companies' / 'suggest'

        params = {'query': query}
        res = requests.get(url, params=params)
        res.raise_for_status()

        return res.json()

    def get_people(self, company: Company, role: Role):
        # Example: https://connect.clearbit.com/v1/people/domain/patreon.com?role=real_estate
        url = _API_BASE / 'people' / 'domain' / company.domain
        params = {'role': role}

        headers = {
            "cookie": f'rack.sessionv2={self.session_id}'
        }

        res = requests.get(url, params=params, headers=headers)
        res.raise_for_status()

        people = res.json()
        for person in people:
            del person['avatar']
            full_name = person['name']['fullName']
            person['first_name'] = full_name.split(' ')[0]
            person['last_name'] = " ".join(full_name.split(' ')[1:])
            person['name'] = full_name

        return people
