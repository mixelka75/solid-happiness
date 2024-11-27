import csv
import re
from datetime import datetime
import format


def get_cleaned_arrow():
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
            return 0 <= age <= 150 and bday != '1900-01-01'
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

    # Проверка СНИЛС (может отсутствовать)
    def is_valid_snils(snils):
        if not snils:  # Если СНИЛС отсутствует, это валидно
            return True
        
        # Удаляем пробелы и проверяем формат
        clean_snils = snils.replace(' ', '').replace('-', '')
        if not clean_snils.isdigit() or len(clean_snils) != 11:
            return False
        
        # Проверяем контрольное число
        number_part = clean_snils[:9]
        control_number = int(clean_snils[9:])
        
        # Если СНИЛС в диапазоне ниже 001-001-998, контрольное число не вычисляется
        if int(number_part) < 1001998:
            return True

        # Вычисляем контрольное число
        checksum = sum(int(digit) * weight for digit, weight in zip(number_part, range(9, 0, -1)))
        calculated_control = checksum % 101
        if calculated_control == 100:
            calculated_control = 0

        return calculated_control == control_number

    # Проверка ИНН (может отсутствовать)
    def is_valid_inn(inn):
        if not inn:  # Если ИНН отсутствует, это валидно
            return True
        
        # Проверяем, что ИНН состоит только из цифр и имеет длину 10 или 12
        if not inn.isdigit() or len(inn) not in (10, 12):
            return False
        
        # Проверка контрольного числа для ИНН физических лиц (12 цифр)
        if len(inn) == 12:
            def calculate_check_digit(inn_part, weights):
                return sum(int(digit) * weight for digit, weight in zip(inn_part, weights)) % 11 % 10

            n11 = calculate_check_digit(inn[:11], [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0])
            n12 = calculate_check_digit(inn[:11] + str(n11), [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0])
            return n12 == int(inn[-1])

        # Проверка контрольного числа для ИНН юридических лиц (10 цифр)
        if len(inn) == 10:
            weights = [2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
            checksum = sum(int(digit) * weight for digit, weight in zip(inn, weights)) % 11 % 10
            return checksum == int(inn[-1])

        return False

    # Основной блок
    records = {}

    rrrrrrr = []

    with open('ds_dirty_fin_202410041147.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Чтение и фильтрация данных
        for record in reader:
            phone = record.get('contact_phone', '')
            bday = record.get('client_bday', '')
            gender = record.get('client_gender', '')
            email = record.get('contact_email', '')
            snils = record.get('client_snils', '')
            inn = record.get('client_inn', '')


            # Применение всех проверок
            if (is_valid_phone(phone)
                    and is_valid_bday(bday)
                    and is_valid_gender(gender)
                    and is_valid_email(email)
                    and is_valid_snils(snils)
                    and is_valid_inn(inn)):
                client_id = record['client_id']
                # Добавляем только первую валидную запись для каждого client_id
                rrrrrrr.append(format.dict_to_formated_dict(record))
    return rrrrrrr
