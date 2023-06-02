import clearbit
import pandas as pd


def fuzzy_in(haystack, needles):
    for needle in needles:
        if needle.lower() in haystack.lower():
            return True
    return False


existing_contacts = pd.read_csv('contacts.csv')

cbs = clearbit.ClearBitSession(session_id='83ee5038418c5ed535ff0e5e5f7704b8e9561f9f86dd8563391aa220d341c0f1')

company = cbs.get_top_company('Cockroach Labs')
people = cbs.get_people(company, clearbit.Role.RECRUITING)
people += cbs.get_people(company, clearbit.Role.ENGINEERING)

# points system
for person in people:
    person["favorable_ranking"] = 1000

    # technical evangelists or advocates
    if fuzzy_in(person['title'], ['evangelist', 'advocate']):
        person["favorable_ranking"] += 500

    # campus or university recruiters
    if fuzzy_in(person['title'], ['campus', 'university']):
        person["favorable_ranking"] += 100

    # recruiters
    if fuzzy_in(person['title'], ['recruiter', 'recruiting', 'talent']):
        person["favorable_ranking"] += 50

    # points for being technical
    if fuzzy_in(person['title'], ['technical']):
        person["favorable_ranking"] += 20

    # subtract points for diversity and inclusion
    if fuzzy_in(person['title'], ['diversity', 'inclusion', "de&i", "dei", "d&i"]):
        person["favorable_ranking"] -= 20

    # subtract points for very high level titles
    if fuzzy_in(person['title'], ['senior', 'vp', 'director', 'head', 'lead', 'executive', 'chief', 'principal']):
        person["favorable_ranking"] -= 10

    # subtract points for very lower, but still senior titles
    if fuzzy_in(person['title'], ['manager', 'associate', 'assistant', 'coordinator', 'specialist']):
        person["favorable_ranking"] -= 5


people.sort(key=lambda x: x['favorable_ranking'], reverse=True)

# print out the top 10
# create a df
df = pd.DataFrame(people)
print(df.head(5))


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
