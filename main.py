

def get_gold(filename,result_filename):
    import deleting, duble, pohoz, app, os, csv

    app.update_status(filename, 'Очищаю записи...')
    cleaned_arrow = deleting.get_cleaned_arrow(filename)

    app.update_status(filename, 'Ищу золотые записи среди похожих...')
    pohoz =pohoz.process_records(cleaned_arrow)

    app.update_status(filename, 'Ищу золотые записи среди дубликатов...')
    duble = duble.group_related_records(cleaned_arrow)

    app.update_status(filename, 'Объединяю массивы..')

    import json

    import csv
    import os

    def union_dicts_to_csv(list1, list2, filename):
        seen = set()
        result = []
        
        # Задаем порядок столбцов
        keys = [
            "client_id", "client_first_name", "client_middle_name", "client_last_name",
            "client_fio_full", "client_bday", "client_bplace", "client_cityzen",
            "client_resident_cd", "client_gender", "client_marital_cd", "client_graduate",
            "client_child_cnt", "client_mil_cd", "client_zagran_cd", "client_inn",
            "client_snils", "client_vip_cd", "contact_vc", "contact_tg", "contact_other",
            "contact_email", "contact_phone", "addr_region", "addr_country", "addr_zip",
            "addr_street", "addr_house", "addr_body", "addr_flat", "addr_area",
            "addr_loc", "addr_city", "addr_reg_dt", "addr_str", "fin_rating",
            "fin_loan_limit", "fin_loan_value", "fin_loan_debt", "fin_loan_percent",
            "fin_loan_begin_dt", "fin_loan_end_dt", "stream_favorite_show",
            "stream_duration", "create_date", "update_date", "source_cd"
        ]
        
        for lst in (list1, list2):
            for d in lst:
                fs = frozenset(d.items())
                if fs not in seen:
                    seen.add(fs)
                    result.append(d)
        
        # Убедимся, что папка 'results' существует
        os.makedirs('results', exist_ok=True)
        filepath = os.path.join('results', filename)
        
        # Запись в CSV файл
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(result)



    union_dicts_to_csv(duble,pohoz, result_filename)
    app.update_status(filename, f'http://127.0.0.1:8000/results/{result_filename}')