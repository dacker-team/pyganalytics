from dbstream import DBStream


def send_to_db(dbstream: DBStream, data, all_batch_id):
    all_batch_id = ["'" + e + "'" for e in all_batch_id]
    table_name = data["table_name"]
    if all_batch_id:
        # try:
            query = "DELETE FROM %s WHERE batch_id IN (%s);" % (table_name, ",".join(all_batch_id))
            dbstream.execute_query(query)
        # except:
        #     print("Table does not exist")
    data["columns_name"] = [r.replace(":", "_") for r in data["columns_name"]]
    print(data)
    dbstream.send_data(data, replace=False)
