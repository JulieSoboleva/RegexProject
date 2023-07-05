import re
import csv


def split_names(contacts):
    for person_list in contacts:
        for i, _ in enumerate(person_list):
            parts = person_list[0].split()
            if len(parts) > 1:
                person_list[0] = parts[0]
                person_list[1] = parts[1]
                if len(parts) > 2:
                    person_list[2] = parts[2]
            parts = person_list[1].split()
            if len(parts) > 1:
                person_list[1] = parts[0]
                person_list[2] = parts[1]
    return contacts


def list_to_dict(contacts):
    result = {}
    for person in contacts:
        key = f'{person[0]} {person[1]}'
        current_contact = [x for x in person[2:]]
        if result.get(key) is None:
            result[key] = current_contact
        else:
            result[key] = [y if x == '' else x for x, y
                           in zip(result.get(key), current_contact)]
    return result


def format_phones(contacts):
    pattern = r'(\+7|8)\s*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*' \
              r'(\d{2})[\s-]*(\d{2})\s*\(*(доб.)*\s*(\d{4})*\)*'
    repl = r'+7(\2)\3-\4-\5 \6\7'
    for data in contacts.values():
        data[3] = re.sub(pattern, repl, data[3]).strip()
    return contacts


def dict_to_list(contacts):
    result = []
    for key, value in contacts.items():
        person = key.split()
        person.extend(value)
        result.append(person)
    return result


if __name__ == '__main__':
    csv.register_dialect('custom_csv', delimiter=',',
                         quoting=csv.QUOTE_MINIMAL)
    with open('phonebook_raw.csv', encoding='utf-8') as f:
        contacts_list = list(csv.reader(f, delimiter=','))

    contacts_list = split_names(contacts_list)
    contacts_dict = list_to_dict(contacts_list)
    contacts_dict = format_phones(contacts_dict)
    contacts_list = dict_to_list(contacts_dict)

    with open('phonebook.csv', 'w', encoding='utf-8') as f:
        datawriter = csv.writer(f, 'custom_csv')
        datawriter.writerows(contacts_list)
