import pandas as pd


def create_import_template(columns):
    return pd.DataFrame(columns=columns)


def read_sheet(data, sheet_name, skip_rows=1):
    try:
        sheet_data = pd.read_excel(io=data, sheet_name=sheet_name, skiprows=skip_rows)
        sheet_data = sheet_data.dropna(how="all")
        return sheet_data
    except ValueError:
        return pd.DataFrame()


def remove_placeholders(data, column_header, placeholders):
    try:
        data = data[~data[column_header].isin(placeholders)]
        return data
    except KeyError:
        return data
