import copy

from dbstream import DBStream


def send_to_db(dbstream: DBStream, data, all_batch_id):
    all_batch_id = ["'" + e + "'" for e in all_batch_id]
    table_name = data["table_name"]
    if all_batch_id:
        try:
            query = "DELETE FROM %s WHERE batch_id IN (%s);" % (table_name, ",".join(all_batch_id))
            dbstream.execute_query(query)
        except:
            print("Table does not exist")
    data["columns_name"] = [r.replace(":", "_") for r in data["columns_name"]]
    copy_data = copy.deepcopy(data)
    total_length = len(copy.deepcopy(data)["rows"])
    try:
        dbstream.send_data(data, replace=False)
    except:
        i = 0
        while i < total_length:
            small_rows = copy_data["rows"][i:i + 50]
            print(small_rows)
            dbstream.send_data({
                "table_name": copy_data["table_name"],
                "columns_name": copy_data["columns_name"],
                "rows": small_rows
            }, replace=False)
            i = i + 50
