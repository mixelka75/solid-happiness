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
x = {
        "client_id": 807719023,
        "client_first_name": "Хабибат",
        "client_middle_name": "Махмашариповна",
        "client_last_name": "Чичева",
        "client_fio_full": "Чичева Хабибат Махмашариповна",
        "client_bday": "1948-04-16",
        "client_bplace": "",
        "client_cityzen": "",
        "client_resident_cd": None,
        "client_gender": "Ж",
        "client_marital_cd": None,
        "client_graduate": "",
        "client_child_cnt": 1,
        "client_mil_cd": None,
        "client_zagran_cd": "",
        "client_inn": "",
        "client_snils": "",
        "client_vip_cd": "",
        "contact_vc": "",
        "contact_tg": "",
        "contact_other": "",
        "contact_email": "hiheva@dirtythird.com",
        "contact_phone": "+7 951 900 3326",
        "addr_region": "",
        "addr_country": "",
        "addr_zip": "",
        "addr_street": "",
        "addr_house": "",
        "addr_body": "",
        "addr_flat": "",
        "addr_area": "",
        "addr_loc": "",
        "addr_city": "",
        "addr_reg_dt": "",
        "addr_str": "hiheva@dirtythird.com",
        "fin_rating": None,
        "fin_loan_limit": None,
        "fin_loan_value": None,
        "fin_loan_debt": None,
        "fin_loan_percent": None,
        "fin_loan_begin_dt": "2021-04-08 10:05:54.722",
        "fin_loan_end_dt": "2021-04-08 10:05:54.722",
        "stream_favorite_show": "Once Upon a Time in Hollywood",
        "stream_duration": 407,
        "create_date": "2021-04-08 10:05:54.722",
        "update_date": "2021-04-08 10:05:54.722",
        "source_cd": "Stream"
    }


fields_for_format = ['client_id', 'client_first_name', 'client_middle_name', 'client_last_name',
                     'client_fio_full', 'client_bday', 'client_bplace', 'client_cityzen', 'client_cityzen',
                     'contact_email', 'contact_phone', 'create_date', 'update_date']


def _check_bdata_or_ymd(data: str) -> str | None:
    try:
        datetime.datetime.strptime(data, "%Y %m %d")
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


def dict_to_formated_dict(kwarg: dict) -> dict:

    formatting_rules = {
        "client_id": lambda x: x,
        "client_first_name": lambda x: x.title(),
        "client_middle_name": lambda x: x.title(),
        "client_last_name": lambda x: x.title(),
        "client_fio_full": lambda x: x if len(x.split()) == 3 else None,
        "client_bday": lambda x: _check_bdata_or_ymd(str(x)),
        "client_bplace": lambda x: x,
        "client_cityzen": lambda x: x.upper(),
        "contact_email": lambda x: x.lower(),
        "contact_phone": lambda x: x if len(''.join(x.split()))-1 == 12 else None,
        "create_date": lambda x: _check_data(str(x)),
        "update_date": lambda x: _check_data(str(x))
    }

    format_dict = {key: formatting_rules[key](value)
                    if key in fields_for_format and formatting_rules[key](value) is not None else value
                    for key, value in kwarg.items()}

    return format_dict if len(kwarg) == len(format_dict) else None

print(dict_to_formated_dict(x))