import re
import csv
from pprint import pprint


csv.register_dialect('custom_csv', delimiter=',', quoting=csv.QUOTE_MINIMAL)
with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)

person_list = []
for i, _ in enumerate(contacts_list):
    if i == 0:
        continue
    person_list.append({'lastname': contacts_list[i][0],
                        'firstname': contacts_list[i][1],
                        'surname': contacts_list[i][2],
                        'organization': contacts_list[i][3],
                        'position': contacts_list[i][4],
                        'phone': contacts_list[i][5],
                        'email': contacts_list[i][6]})

pattern = r'(\+7|8)\s*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(*(доб.)*\s*(\d{4})*\)*'
repl = r'+7(\2)\3-\4-\5 \6\7'
for i, _ in enumerate(person_list):
    parts = person_list[i]['lastname'].split()
    if len(parts) > 1:
        person_list[i]['lastname'] = parts[0]
        person_list[i]['firstname'] = parts[1]
        if len(parts) > 2:
            person_list[i]['surname'] = parts[2]
    parts = person_list[i]['firstname'].split()
    if len(parts) > 1:
        person_list[i]['firstname'] = parts[0]
        person_list[i]['surname'] = parts[1]
    person_list[i]['phone'] = re.sub(pattern, repl, person_list[i]['phone']).strip()
# pprint(person_list)

pure_contacts_list = [contacts_list[0]]


def person_index(lastname, firstname, contacts):
    for ind, _ in enumerate(contacts):
        if (lastname == contacts[ind][0] and
                firstname == contacts[ind][1]):
            return ind
    return -1


for i, _ in enumerate(person_list):
    pos = person_index(person_list[i]['lastname'], person_list[i]['firstname'],
                       pure_contacts_list)
    if pos < 0:
        pure_contacts_list.append([person_list[i]['lastname'],
                                   person_list[i]['firstname'],
                                   person_list[i]['surname'],
                                   person_list[i]['organization'],
                                   person_list[i]['position'],
                                   person_list[i]['phone'],
                                   person_list[i]['email']])
    else:
        for j, _ in enumerate(pure_contacts_list[pos]):
            if pure_contacts_list[pos][j] == '':
                match j:
                    case 2:
                        pure_contacts_list[pos][j] = person_list[i]['surname']
                    case 3:
                        pure_contacts_list[pos][j] = person_list[i]['organization']
                    case 4:
                        pure_contacts_list[pos][j] = person_list[i]['position']
                    case 5:
                        pure_contacts_list[pos][j] = person_list[i]['phone']
                    case 6:
                        pure_contacts_list[pos][j] = person_list[i]['email']
                    case _:
                        pass

# pprint(pure_contacts_list)

with open('phonebook.csv', 'w', encoding='utf-8') as f:
    datawriter = csv.writer(f, 'custom_csv')
    datawriter.writerows(pure_contacts_list)
