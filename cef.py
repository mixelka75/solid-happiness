from datetime import datetime

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

# Example usage:
records = [
    {
        'client_id': '205377422',
        'client_first_name': 'мухаят',
        'client_middle_name': '',
        'client_last_name': '',
        'update_date': '2018-04-23 00:26:28.302',
        # Other fields...
    },
    {
        'client_id': '205377422',
        'client_first_name': 'Мухаят',
        'client_middle_name': 'Самуэловна',
        'client_last_name': 'Каранкевич',
        'update_date': '2019-06-15 12:00:00.000',
        # Other fields...
    },
    {
        'client_id': '205377422',
        'client_first_name': '',
        'client_middle_name': 'Самуэловна',
        'client_last_name': '',
        'client_bday': '1992-06-11',
        'update_date': '2020-01-10 08:30:00.000',
        # Other fields...
    },
    # Add other records as needed
]

golden_record = merge_records(records)
print("Golden Record:")
for key, value in golden_record.items():
    print(f"{key}: {value}")
