import deleting, duble, pohoz


print('чистые получаю')
cleaned_arrow = deleting.get_cleaned_arrow()

print('золотые записи получаю похожие')
pohoz =pohoz.process_records(cleaned_arrow)


print('золотые записи получаю дублированные')
duble = duble.group_related_records(cleaned_arrow)

print('объединение')

import json

def union_dicts_to_json(list1, list2, filename):
    seen = set()
    result = []
    for lst in (list1, list2):
        for d in lst:
            fs = frozenset(d.items())
            if fs not in seen:
                seen.add(fs)
                result.append(d)
    # Запись в JSON файл
    print(f'всего элементов: {len(result)}')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


union_dicts_to_json(duble,pohoz, 'armanSila.json')