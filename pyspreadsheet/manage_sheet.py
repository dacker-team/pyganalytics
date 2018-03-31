from . import init_connection


def get_sheet_info(sheet_id):
    account = init_connection.get_api_account()
    sheet = account.get(
        spreadsheetId=sheet_id
    ).execute()
    return sheet


def find_worksheet(sheet_id, worksheet_name):
    sheet = get_sheet_info(sheet_id)
    wks_list = sheet.get("sheets")
    for wks in wks_list:
        if wks.get("properties").get("title").lower() == worksheet_name.lower():
            return wks
    print("This worksheet doesn't exist")
    return None


def add_worksheet(sheet_id, worksheet_name):
    account = init_connection.get_api_account()
    requests = [
        {
            "addSheet": {
                "properties": {
                    "title": worksheet_name,
                    "tabColor": {
                        "red": 0.0,
                        "green": 0.0,
                        "blue": 1.0
                    }
                }
            }
        }
    ]
    body = {
        'requests': requests
    }
    response = account.batchUpdate(spreadsheetId=sheet_id,
                                 body=body).execute()
    return response
