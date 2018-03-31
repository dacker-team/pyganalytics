import pandas

from .tool import column_string, construct_range
from .init_connection import get_api_account


def get_data_from_range(sheet_id, worksheet_name, nb_column, nb_row):
    range = construct_range(worksheet_name, "A1", column_string(nb_column) + str(nb_row + 1))
    account = get_api_account()
    data = account.values().get(
        spreadsheetId=sheet_id,
        range=range
    ).execute()
    return data


def check_first_row(values, columns_name):
    nb_column = len(columns_name)
    first_row = values[0]
    column_index_to_investigate = []
    for i in range(nb_column):
        try:
            column_name = first_row[i]
            if column_name != columns_name[i]:
                column_index_to_investigate.append(i)
        except IndexError:
            column_index_to_investigate.append(i)
    return column_index_to_investigate


def check_other_row(column_index_to_investigate, values):
    df = pandas.DataFrame(values[1:])
    warning_columns = []
    for i in column_index_to_investigate:
        try:
            boolean_list = list(pandas.isnull(df[i].replace(to_replace=[""], value=[None])))
            if not all(boolean_list):
                warning_columns.append(i)

        except KeyError:
            pass
    return warning_columns


def check_availability_column(sheet_id, data):
    worksheet_name = data["worksheet_name"]
    columns_name = data["columns_name"]
    rows = data["rows"]
    nb_row = len(rows)
    nb_column = len(columns_name)
    data = get_data_from_range(sheet_id, worksheet_name, nb_column, nb_row)
    completely_available = {
        "completely_available": True
    }
    values = data.get("values")
    if not values:
        return completely_available
    response = {
        "completely_available": False
    }
    column_index_to_investigate = check_first_row(values, columns_name)
    warning_columns = check_other_row(column_index_to_investigate, values)
    if not warning_columns:
        return completely_available
    warning_columns = [column_string(wc + 1) for wc in warning_columns]
    response["warning_columns"] = warning_columns
    return response
