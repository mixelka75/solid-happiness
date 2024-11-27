import csv
import re
from datetime import datetime
import format

# Проверка номера телефона
def is_valid_phone(phone):
    phone = str(phone)  # Приведение к строке
    clean_phone = phone.replace(' ', '').replace('+', '')
    if clean_phone.startswith('8'):
        clean_phone = '7' + clean_phone[1:]
    return clean_phone.isdigit() and len(clean_phone) == 11

# Проверка возраста по дате рождения
def is_valid_bday(bday):
    try:
        bday_date = datetime.strptime(bday, '%Y-%m-%d')
        age = (datetime.now() - bday_date).days // 365
        return 0 <= age <= 200 and bday != '1900-01-01'
    except ValueError:
        return False

# Проверка пола (английский и русский варианты)
def is_valid_gender(gender):
    valid_genders = {'M', 'F', 'Male', 'Female', 'm', 'f', 
                     'М', 'Ж', 'м', 'ж', 'Мужчина', 'Женщина'}
    return gender in valid_genders

# Проверка email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# Основной блок
result_dict_list = []

with open('ds_dirty_fin_202410041147.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Заголовки CSV как ключи для словаря

    # Индексы полей
    phone_index = headers.index('contact_phone')
    bday_index = headers.index('client_bday')
    gender_index = headers.index('client_gender')
    email_index = headers.index('contact_email')

    for row in reader:
        phone = row[phone_index]
        bday = row[bday_index]
        gender = row[gender_index]
        email = row[email_index]

        # Применение всех проверок
        if (is_valid_phone(phone)
                and is_valid_bday(bday)
                and is_valid_gender(gender)
                and is_valid_email(email)
                and row.count('') <= 0.2 * len(row)):
            # Создание словаря из строки
            row_dict = dict(zip(headers, row))
            row_dict = format.dict_to_formated_dict(row_dict)
            result_dict_list.append(row_dict)

# Теперь `result_dict_list` содержит список словарей с проверенными данными


print(result_dict_list[0])
