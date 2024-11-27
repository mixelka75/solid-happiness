from collections import defaultdict
import re
from datetime import datetime
from duble import merge_records

def normalize_name(name):
    return re.sub(r'\s+', '', name.lower())

def normalize_phone(phone):
    return re.sub(r'\D', '', phone)

def normalize_email(email):
    return email.strip().lower()

def compare_records(record1, record2):
    # Определяем поля для сравнения и их веса
    fields = [
        ('client_first_name', normalize_name, 1),
        ('client_middle_name', normalize_name, 1),
        ('client_last_name', normalize_name, 1),
        ('client_bday', lambda x: x, 2),
        ('client_inn', lambda x: x, 2),
        ('client_snils', lambda x: x, 2),
        ('contact_phone', normalize_phone, 1),
        ('contact_email', normalize_email, 1)
    ]
    
    total_weight = sum(weight for _, _, weight in fields)
    total_similarity = 0
    
    for field_name, normalizer, weight in fields:
        val1 = record1.get(field_name, '')
        val2 = record2.get(field_name, '')
        if not val1 or not val2:
            continue
        norm_val1 = normalizer(val1)
        norm_val2 = normalizer(val2)
        if norm_val1 == norm_val2:
            total_similarity += weight
    
    similarity_percentage = (total_similarity / total_weight) * 100
    return similarity_percentage

def build_blocks(records):
    # Создаём блоки по ключевым полям
    blocks = defaultdict(list)
    for idx, record in enumerate(records):
        # Используем комбинацию нормализованных имени и даты рождения в качестве ключа блока
        name_key = normalize_name(record.get('client_last_name', '') + record.get('client_first_name', ''))
        bday_key = record.get('client_bday', '')
        block_key = name_key + bday_key
        blocks[block_key].append((idx, record))
    return blocks

def process_records(records):
    blocks = build_blocks(records)
    visited = set()
    golden_records = []
    
    for block in blocks.values():
        # Внутри каждого блока сравниваем записи попарно
        n = len(block)
        component = []
        for i in range(n):
            idx_i, rec_i = block[i]
            if idx_i in visited:
                continue
            group = [rec_i]
            visited.add(idx_i)
            for j in range(i+1, n):
                idx_j, rec_j = block[j]
                if idx_j in visited:
                    continue
                similarity = compare_records(rec_i, rec_j)
                if similarity >= 60:
                    group.append(rec_j)
                    visited.add(idx_j)
            # Вызываем merge_records для группы похожих записей
            golden_record = merge_records(group)
            golden_records.append(golden_record)
    return golden_records

# Пример использования
if __name__ == '__main__':
    records = [
        {'client_id': '596118586', 'client_first_name': 'меджид', 'client_middle_name': 'кузарович', 'client_last_name': 'евдунов', 'client_fio_full': 'евдунов меджид кузарович', 'client_bday': '1992-08-23', 'client_bplace': 'дер. киргинцево аромашевского р-на тюменской обл.', 'client_cityzen': 'rus', 'client_resident_cd': 'Д', 'client_gender': 'М', 'client_marital_cd': 'Д', 'client_graduate': 'Н', 'client_child_cnt': '2', 'client_mil_cd': 'Д', 'client_zagran_cd': 'Н', 'client_inn': '912343465984', 'client_snils': '52203201188', 'client_vip_cd': 'Н', 'contact_vc': '', 'contact_tg': '', 'contact_other': '', 'contact_email': 'evdunov@goddess.com', 'contact_phone': '+7 926 226 7251', 'addr_region': '63', 'addr_country': '1103', 'addr_zip': '445039', 'addr_street': 'гая', 'addr_house': '12', 'addr_body': '', 'addr_flat': '318', 'addr_area': '', 'addr_loc': '', 'addr_city': 'тольятти', 'addr_reg_dt': '', 'addr_str': '63, г.тольятти, ул. гая, д.12, кв.318', 'fin_rating': '5', 'fin_loan_limit': '729900', 'fin_loan_value': '', 'fin_loan_debt': '', 'fin_loan_percent': '', 'fin_loan_begin_dt': '', 'fin_loan_end_dt': '', 'stream_favorite_show': '', 'stream_duration': '', 'create_date': '2020-07-16 05:10:57.904', 'update_date': '2020-07-16 05:10:57.904', 'source_cd': 'Bank'}
        # Добавьте дополнительные записи по необходимости
    ]
    
    # Предположим, что функция merge_records определена где-то ещ
    
    golden_records = process_records(records)
    
    for record in golden_records:
        print(record)
