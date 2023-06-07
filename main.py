import clearbit
import clipboard
import pandas as pd


def fuzzy_in(haystack, needles):
    for needle in needles:
        if needle.lower() in haystack.lower():
            return True
    return False


existing_contacts = pd.read_csv('contacts.csv')

cbs = clearbit.ClearBitSession(session_id='83ee5038418c5ed535ff0e5e5f7704b8e9561f9f86dd8563391aa220d341c0f1')

company = cbs.get_top_company('twilio.com')
people = cbs.get_people(company, clearbit.Role.RECRUITING)
people += cbs.get_people(company, clearbit.Role.ENGINEERING)

# points system
for person in people:
    person["quality_score"] = 1000

    # technical evangelists or advocates
    if fuzzy_in(person['title'], ['evangelist', 'advocate']):
        person["quality_score"] += 500

    # campus or university recruiters
    if fuzzy_in(person['title'], ['campus', 'university']):
        person["quality_score"] += 100

    # recruiters
    if fuzzy_in(person['title'], ['recruiter', 'recruiting', 'talent', 'sourcing', 'sourcer']):
        person["quality_score"] += 50

    # points for being technical
    if fuzzy_in(person['title'], ['technical']):
        person["quality_score"] += 20

    # subtract points for being global or international
    if fuzzy_in(person['title'], ['global', 'international', 'worldwide']):
        person["quality_score"] -= 10

    # subtract points for diversity and inclusion
    if fuzzy_in(person['title'], ['diversity', 'inclusion', "de&i", "dei", "d&i"]):
        person["quality_score"] -= 20

    # subtract points for very high level titles
    if fuzzy_in(person['title'], ['senior', 'vp', 'director', 'head', 'lead', 'executive', 'chief', 'principal']):
        person["quality_score"] -= 10

    # subtract points for very lower, but still senior titles
    if fuzzy_in(person['title'], ['manager', 'associate', 'assistant', 'coordinator', 'specialist']):
        person["quality_score"] -= 5


people.sort(key=lambda x: x['quality_score'], reverse=True)

if len(people) > 1:
    print("Top result email: ", end="")
    print(cbs.get_person_info(people[0]['id'])['email'])
    print()

# print out the top 10
# create a df
df = pd.DataFrame(people)
df = df[["name", "title", "quality_score"]]
print(df.head(5).to_markdown())

print()
print("Company Details")
print("---------------")
print(f"Name: {company.name}")
print(f"Domain: {company.domain}")
print(f"Employees: {company.size}")
print(f"Type: {'Big Tech' if company.size > 10000 else 'Tech'}")

# Asana	Tech	Casey	Goodman	caseygoodman@asana.com		Not Contacted Yet		Recruiting
# Twilio  Tech    Lizzie Siegle   lsiegle@twilio.com              Not Contacted Yet               Developer Evangelist Lll
clipboard.copy(
    f"{company.name}\t"
    f"Tech\t{people[0]['first_name']}\t{people[0]['last_name']}\t"
    f"{cbs.get_person_info(people[0]['id'])['email']}\t\t"
    f"Not Contacted Yet\t\t{people[0]['title']}"
)

print("Success! Copied to clipboard.")


# campus_recruiters = []
# campus_di_recruiters = []
# senior_recruiters = []
# other_recruiters = []
# other_di_recruiters = []

# for person in people:
#     if fuzzy_in(person['title'], ['campus', 'university']):
#         if fuzzy_in(person['title'], ['diversity', 'inclusion', "de&i", "dei", "d&i"]):
#             campus_di_recruiters.append(person)
#         else:
#             campus_recruiters.append(person)

#     elif fuzzy_in(person['title'],
#                   ['senior', 'vp', 'manager', 'director', 'head', 'lead', 'executive', 'chief', 'principal']):
#         senior_recruiters.append(person)
#     else:
#         if fuzzy_in(person['title'], ['diversity', 'inclusion', "de&i", "dei", "d&i"]):
#             other_di_recruiters.append(person)
#         else:
#             other_recruiters.append(person)

# campus_recruiters.sort(key=lambda x: x['title'])
# campus_di_recruiters.sort(key=lambda x: x['title'])
# senior_recruiters.sort(key=lambda x: x['title'])
# other_recruiters.sort(key=lambda x: x['title'])
# other_di_recruiters.sort(key=lambda x: x['title'])

# print("\nCAMPUS RECRUITERS")
# print("\n".join(map(lambda x: x["title"], campus_recruiters)))

# print("\nCAMPUS D&I RECRUITERS")
# print("\n".join(map(lambda x: x["title"], campus_di_recruiters)))

# print("\nOTHER RECRUITERS")
# print("\n".join(map(lambda x: x["title"], other_recruiters)))

# print("\nSENIOR RECRUITERS")
# print("\n".join(map(lambda x: x["title"], senior_recruiters)))

# print("\nOTHER D&I RECRUITERS")
# print("\n".join(map(lambda x: x["title"], other_di_recruiters)))
