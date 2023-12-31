import re
from pprint import pprint
import csv
from collections import OrderedDict

def search_names(contacts_list, row, num):
    '''Проверка на имя в первых трёх полях'''

    last_first_sur_name = " ".join(row[:3])
    pattern = re.compile("[А-ЯЁ][а-яё]\w+")
    name_parts = re.findall(pattern, last_first_sur_name)

    for seq, name in enumerate(name_parts):
        contacts_list[num][seq] = name

def search_phones(contacts_list, row, num):
    '''Поиск номера и его замена'''
    
    try:
        row_str = " ".join(row)
        
        if "доб" in row_str:
            
            pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?[-]?(\d{3})\s?[-]?(\d{2})[-]?(\d+)\s?\(?(доб\.)\s(\d+)\)?"
            sub = r"+7(\2)\3-\4-\5 \6\7"

            spec_pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?[-]?(\d{3})\s?[-]?(\d{2})[-]?(\d+)\s(доб\.)(\d+)"
        else:
            pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?[-]?(\d{3})\s?[-]?(\d{2})[-]?(\d+)"
            sub = r"+7(\2)\3-\4-\5"
            spec_pattern = pattern

        correct_row = re.compile(pattern).sub(sub, row_str)
        phone_number = re.search(spec_pattern, correct_row).group()
        contacts_list[num][-2] = phone_number

    except AttributeError:
        pass

def remove_doubles(contacts_list, new_contacts_list):
    for row_num, contact in enumerate(contacts_list):
        if row_num != len(contacts_list):
                for item in contacts_list[row_num + 1:]:
                    if contact[0] in item and contact[1] in item:
                        difference = sorted(set(item).difference(set(contact)))

                        for diff in difference:
                            if re.search(r"(\+7|8)", diff) is not None:
                                contact[-2] = diff
                            elif re.search(r"@", diff) is not None:
                                contact[-1] = diff
                            else:
                                if contact[-3] == '':
                                    contact[-3] = diff
                                else:
                                    contact[-4] = diff

                        new_contacts_list += [contact]
                        contacts_list.remove(contact)
                        contacts_list.remove(item)

def main():
    with open("regural_expressions/phonebook_raw.csv") as file:
        rows = csv.reader(file, delimiter=',')
        contacts_list = list(rows)

    headers = ['lastname',
        'firstname',
        'surname',
        'organization',
        'position',
        'phone',
        'email'
        ]
    contacts_list.remove(headers)
    new_contacts_list = [headers]
    
    for num, row in enumerate(contacts_list):
        search_names(contacts_list, row, num)
        search_phones(contacts_list, row, num)

    remove_doubles(contacts_list, new_contacts_list)
    new_contacts_list.extend(contacts_list)

    with open("regural_expressions/phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(new_contacts_list)
    
if __name__ == '__main__':
    main()