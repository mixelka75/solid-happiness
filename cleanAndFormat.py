import pandas as pd
import re
from datetime import datetime

# Read the CSV file
df = pd.read_csv('ds_dirty_fin_202410041147.csv', encoding='utf-8')

# Validation functions using vectorized operations

# Validating 'contact_phone'
df['contact_phone'] = df['contact_phone'].astype(str)
clean_phones = df['contact_phone'].str.replace(' ', '').str.replace('+', '')
clean_phones = clean_phones.where(~clean_phones.str.startswith('8'), '7' + clean_phones.str[1:])
valid_phone = clean_phones.str.isdigit() & (clean_phones.str.len() == 11)

# Validating 'client_bday' without causing OverflowError
bday_dates = pd.to_datetime(df['client_bday'], format='%Y-%m-%d', errors='coerce')
current_date = pd.Timestamp.now()

age = current_date.year - bday_dates.dt.year - (
    (current_date.month, current_date.day) < (bday_dates.dt.month, bday_dates.dt.day)
)

valid_bday = (
    (age >= 0) & (age <= 200) & (df['client_bday'] != '1900-01-01') & bday_dates.notnull()
)

# Validating 'client_gender'
valid_genders = {
    'M', 'F', 'Male', 'Female', 'm', 'f',
    'М', 'Ж', 'м', 'ж', 'Мужчина', 'Женщина'
}
valid_gender = df['client_gender'].isin(valid_genders)

# Validating 'contact_email' with Unicode support
df['contact_email'] = df['contact_email'].astype(str)
email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
valid_email = df['contact_email'].str.match(email_pattern)

# Validating empty fields (no more than 20% empty)
empty_fields_count = (df.isnull() | (df == '')).sum(axis=1)
valid_row = empty_fields_count <= 0.2 * len(df.columns)

# Combining all validation conditions
valid_rows = valid_phone & valid_bday & valid_gender & valid_email & valid_row

# Filtering the DataFrame
df_valid = df[valid_rows].copy()

# Formatting functions
fields_for_format = [
    'client_id', 'client_first_name', 'client_middle_name', 'client_last_name',
    'client_fio_full', 'client_bday', 'client_bplace', 'client_cityzen',
    'contact_email', 'contact_phone', 'create_date', 'update_date'
]

# 'client_first_name', 'client_middle_name', 'client_last_name' to title case
df_valid['client_first_name'] = df_valid['client_first_name'].str.title()
df_valid['client_middle_name'] = df_valid['client_middle_name'].str.title()
df_valid['client_last_name'] = df_valid['client_last_name'].str.title()

# 'client_fio_full', ensure it has exactly 3 parts
df_valid['client_fio_full'] = df_valid['client_fio_full'].where(
    df_valid['client_fio_full'].str.split().str.len() == 3
)

# 'client_bday', ensure format "%Y %m %d"
df_valid['client_bday'] = pd.to_datetime(df_valid['client_bday'], errors='coerce')
df_valid['client_bday'] = df_valid['client_bday'].dt.strftime('%Y %m %d')

# 'client_cityzen' to upper case
df_valid['client_cityzen'] = df_valid['client_cityzen'].str.upper()

# 'contact_email' to lower case
df_valid['contact_email'] = df_valid['contact_email'].str.lower()

# 'contact_phone', ensure length after removing spaces is 12 (including '+' sign)
df_valid['contact_phone'] = df_valid['contact_phone'].apply(
    lambda x: x if len(''.join(str(x).split())) == 12 else None
)

# Formatting 'create_date' and 'update_date', ensure format "%Y %m %d %H:%M:%S.%f"
def _check_valid_datetime(data):
    try:
        return pd.to_datetime(
            data, format='%Y %m %d %H:%M:%S.%f', errors='raise'
        ).strftime('%Y %m %d %H:%M:%S.%f')
    except (ValueError, TypeError):
        return None

df_valid['create_date'] = df_valid['create_date'].apply(
    lambda x: _check_valid_datetime(str(x))
)
df_valid['update_date'] = df_valid['update_date'].apply(
    lambda x: _check_valid_datetime(str(x))
)

# Dropping rows where formatting resulted in None
df_valid.dropna(subset=fields_for_format, inplace=True)

# Converting DataFrame to a list of dictionaries
result = df_valid.to_dict('records')

# Output: result is a list of dictionaries with keys matching CSV columns
