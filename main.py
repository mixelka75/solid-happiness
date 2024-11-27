

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

    def union_dicts_to_csv(list1, list2, filename):
        seen = set()
        result = []
        keys = set()
        
        for lst in (list1, list2):
            for d in lst:
                fs = frozenset(d.items())
                if fs not in seen:
                    seen.add(fs)
                    result.append(d)
                    keys.update(d.keys())
        
        keys = sorted(keys)  # Сортируем ключи для сохранения порядка столбцов

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