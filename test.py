import dask.dataframe as dd
import pandas as pd
import numpy as np

# Определение типов данных для столбцов с проблемами
dtype_dict = {
    'addr_area': 'object',
    'addr_body': 'object',
    'addr_flat': 'object',
    'addr_house': 'object',
    'addr_loc': 'object232',
    'addr_zip': 'object',
    'contact_tg': 'object',
    'contact_vc': 'object',
    'contact_other': 'object',
    'fin_loan_begin_dt': 'object',
    'fin_loan_end_dt': 'object',
    # Добавьте другие столбцы с проблемами, если они появятся
}

# Загрузка большого CSV файла с использованием Dask
df = dd.read_csv(
    'ds_dirty_fin_202410041147.csv',
    dtype=dtype_dict,
    assume_missing=True,
    low_memory=False
)

# Предобработка данных
def preprocess(df):
    # Преобразование дат
    date_columns = ['create_date', 'update_date', 'client_bday', 'fin_loan_begin_dt', 'fin_loan_end_dt']
    for col in date_columns:
        if col in df.columns:
            df[col] = dd.to_datetime(df[col], errors='coerce')
        else:
            df[col] = None

    # Стандартизация текстовых полей
    text_columns = [
        'client_first_name', 'client_middle_name', 'client_last_name',
        'client_fio_full', 'client_bplace', 'client_cityzen',
        'contact_email', 'contact_phone', 'contact_tg', 'contact_vc',
        'contact_other', 'addr_region', 'addr_country', 'addr_street', 'addr_area',
        'addr_loc', 'addr_city', 'addr_str', 'source_cd',
        'stream_favorite_show'
    ]
    for col in text_columns:
        if col in df.columns:
            # Преобразуем столбец в строковый тип и обрабатываем пропущенные значения
            df[col] = df[col].astype(str).fillna('').str.lower().str.strip()
        else:
            df[col] = ''

    # Обработка пропущенных значений для остальных столбцов
    df = df.fillna('')

    return df

df = preprocess(df)

# Определение ключевых полей для сравнения
key_columns = [
    'client_first_name', 'client_middle_name', 'client_last_name',
    'client_bday', 'client_inn', 'client_snils', 'contact_email',
    'contact_phone', 'contact_tg', 'contact_vc', 'contact_other'
]

# Создание вспомогательной колонки для группировки потенциальных дубликатов
def generate_key(df):
    key_series = df[key_columns].fillna('').astype(str).agg('_'.join, axis=1)
    return key_series

df['group_key'] = generate_key(df)

# Подсчет количества заполненных важных полей
important_fields = [
    'client_first_name', 'client_middle_name', 'client_last_name',
    'client_bday', 'client_inn', 'client_snils', 'contact_email',
    'contact_phone', 'contact_tg', 'contact_vc', 'contact_other',
    'addr_region', 'addr_city', 'addr_street', 'addr_house'
]

df['non_null_count'] = df[important_fields].notnull().sum(axis=1)

# Преобразование 'update_date' в числовой формат для сортировки
df['update_timestamp'] = df['update_date'].astype('int64').fillna(0)

# Создание суммарного скоринга
df['score'] = df['non_null_count']

# Сортировка и удаление дубликатов
df = df.map_partitions(
    lambda partition: partition.sort_values(
        by=['group_key', 'score', 'update_timestamp'],
        ascending=[True, False, False]
    ),
    meta=df._meta
)

# Удаление дубликатов по 'group_key', оставляя первую запись
df = df.drop_duplicates(subset='group_key', keep='first')

# Сохранение результатов
df.compute().to_csv('golden_records.csv', index=False)
