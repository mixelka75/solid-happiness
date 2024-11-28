from datetime import datetime

def group_related_records(records):
    # Ключи, по которым будем искать связи
    keys_of_interest = ['client_inn', 'client_snils', 'contact_email', 'contact_phone']
    
    # Инициализация структуры Union-Find
    parents = [i for i in range(len(records))]
    
    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]  # Сжатие пути
            i = parents[i]
        return i

    def union(i, j):
        pi = find(i)
        pj = find(j)
        if pi != pj:
            parents[pi] = pj  # Объединение

    # Создаем отображение ключ-значение на индексы словарей
    key_value_to_indices = {}
    for idx, record in enumerate(records):
        for key in keys_of_interest:
            value = record.get(key)
            if value:
                key_value = (key, value)
                if key_value not in key_value_to_indices:
                    key_value_to_indices[key_value] = []
                key_value_to_indices[key_value].append(idx)

    # Объединяем связанные словари
    for indices in key_value_to_indices.values():
        first_idx = indices[0]
        for idx in indices[1:]:
            union(first_idx, idx)

    # Формируем группы связанных словарей
    groups = {}
    for idx in range(len(records)):
        parent = find(idx)
        if parent not in groups:
            groups[parent] = []
        groups[parent].append(records[idx])

    # Создаем список золотых записей, объединив записи в каждой группе
    golden_records = []
    for group_records in groups.values():
        golden_record = merge_records(group_records)
        golden_records.append(golden_record)

    # Возвращаем список золотых записей
    return golden_records

def merge_records(records):
    golden_record = {}
    field_update_dates = {}

    for record in records:
        # Parse the record's update date
        record_update_date_str = record.get('update_date')
        if record_update_date_str:
            try:
                record_update_date = datetime.strptime(record_update_date_str, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                # Handle cases where microseconds might be missing
                record_update_date = datetime.strptime(record_update_date_str, '%Y-%m-%d %H:%M:%S')
        else:
            # If no update date is provided, consider it as the earliest date
            record_update_date = datetime.min

        for key, value in record.items():
            if key == 'update_date':
                continue  # Skip the update_date field itself

            # Check if the value is non-empty
            if value and str(value).strip():
                # If the field is not yet in the golden record, add it
                if key not in golden_record:
                    golden_record[key] = value
                    field_update_dates[key] = record_update_date
                else:
                    # If the current record's update date is more recent, update the field
                    if record_update_date > field_update_dates[key]:
                        golden_record[key] = value
                        field_update_dates[key] = record_update_date

    return golden_record

