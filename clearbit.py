from dataclasses import dataclass

from path import Path

import requests
import requests_cache

requests_cache.install_cache('clearbit_cache')


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
    size: int = None


class ClearBitSession:
    def __init__(self, session_id: str):
        self.session_id = session_id

    def get_company_details(self, domain: str):
        # Example: https://connect.clearbit.com/v1/companies/find?domain=kohls.com
        url = _API_BASE / 'companies' / 'find'
        params = {'domain': domain}

        headers = {
            "cookie": f'rack.sessionv2={self.session_id}'
        }

        res = requests.get(url, params=params, headers=headers)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            raise AssertionError(f'No company found for domain: {domain}')

        return res.json()

    def get_top_company(self, query: str):
        companies = self.get_companies(query)

        if len(companies) == 0:
            raise AssertionError(f'No companies found for query: {query}')

        top_company = companies[0]

        company_details = self.get_company_details(top_company['domain'])

        return Company(name=company_details['name'],
                       domain=company_details['domain'],
                       size=company_details['metrics']['employees'])

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

    def get_person_info(self, id: str):
        url = _API_BASE / 'people' / id / 'retrieve'
        headers = {
            "cookie": f'rack.sessionv2={self.session_id}'
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()

        return res.json()
