import googleapiclient

from pyspreadsheet import write
from pyspreadsheet.manage_sheet import add_worksheet
from pyspreadsheet.read import check_availability_column


def send_to_sheet(sheet_id, data):
    try:
        available_response = check_availability_column(sheet_id, data)

    except googleapiclient.errors.HttpError:
        add_worksheet(sheet_id, data["worksheet_name"])
        available_response = {
            "completely_available": True
        }
    available = available_response["completely_available"]
    if not available:
        user_response = input("Columns " +
                              ", ".join(available_response["warning_columns"]) +
                              " will be overwritten, do you want to continue ?" +
                              "\nType yes to continue\n")
        if user_response.lower() not in ["yes", "y"]:
            return 0
    write.write(sheet_id, data)
    return 0
