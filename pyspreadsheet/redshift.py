import pyred
from . import core


def query_to_sheet(sheet_id, worksheet_name, instance, query):
    items = pyred.execute.execute_query(instance, query)
    if not items:
        return 0
    columns_name = list(items[0].keys())
    rows = [list(i.values()) for i in items]
    data = {
        "worksheet_name": worksheet_name,
        "columns_name": columns_name,
        "rows": rows
    }
    core.send_to_sheet(sheet_id, data)
    return 0
