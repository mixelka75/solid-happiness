import datetime

# import pandas as pd
# df = pd.read_csv("ds_dirty_fin_202410041147.csv")
# print(df.iloc[0])

# client_id
# client_first_name
# client_middle_name
# client_last_name
# client_fio_full
# client_bday
# client_bplace
# client_cityzen
# contact_email
# contact_phone
# create_date
# update_date


fields_for_format = ['client_id', 'client_first_name', 'client_middle_name', 'client_last_name',
                     'client_fio_full', 'client_bday', 'client_bplace', 'client_cityzen', 'client_cityzen',
                     'contact_email', 'contact_phone', 'create_date', 'update_date','addr_street', 'addr_house',
                      'addr_body', 'addr_flat', 'addr_area', 'addr_loc', 'addr_city', 'addr_reg_dt', 'addr_str']


def _check_bdata_or_ymd(data: str) -> str | None:
    try:
        datetime.datetime.strptime(data, "%Y-%m-%d")
        return data
    except:
        return None


def _check_valid_time(time: str) -> str | None:
    try:
        datetime.datetime.strptime(time, "%H:%M:%S.%f")
    except:
        return None


def _check_data(data: str) -> str | None:
    check = data.split()
    if _check_bdata_or_ymd(check[0]) and _check_valid_time(check[1]):
        return data
    return None


def dict_to_formated_dict(kwarg: dict) -> dict | None:

    formatting_rules = {
        "client_id": lambda x: x,
        "client_first_name": lambda x: x.lower(),
        "client_middle_name": lambda x: x.lower(),
        "client_last_name": lambda x: x.lower(),
        "client_fio_full": lambda x: x.lower() if len(x.split()) == 3 else None,
        "client_bday": lambda x: _check_bdata_or_ymd(str(x)),
        "client_bplace": lambda x: x.lower(),
        "client_cityzen": lambda x: x.lower(),
        "contact_email": lambda x: x.lower(),
        "contact_phone": lambda x: x if len(''.join(x.split())) == 12 else None,
        "create_date": lambda x: _check_data(str(x)),
        "update_date": lambda x: _check_data(str(x)),
        "addr_street": lambda x: str(x).lower(),
        "addr_house": lambda x: str(x).lower(),
        "addr_body": lambda x: str(x).lower(),
        "addr_flat": lambda x: str(x).lower(),
        "addr_area": lambda x: str(x).lower(),
        "addr_loc": lambda x: str(x).lower(),
        "addr_city": lambda x: str(x).lower(),
        "addr_reg_dt": lambda x: str(x).lower(),
        "addr_str": lambda x: str(x).lower()
    }

    format_dict = {key: formatting_rules[key](value)
                    if key in fields_for_format and formatting_rules[key](value) is not None else value
                    for key, value in kwarg.items()}

    return format_dict if len(kwarg) == len(format_dict) else None
