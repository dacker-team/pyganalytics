import psycopg2
import pyred


def to_redshift(data, all_batch_id, redshift_instance, existing_tunnel):
    all_batch_id = ["'" + e + "'" for e in all_batch_id]
    redshift_table = data["table_name"]
    if all_batch_id:
        if pyred.create.existing_test(redshift_instance, redshift_table, existing_tunnel=existing_tunnel):
            query = 'DELETE FROM ' + redshift_table + ' WHERE batch_id IN ' + "(" + ",".join(all_batch_id) + ")"
            pyred.execute_query(redshift_instance, query, existing_tunnel=existing_tunnel)
    data["columns_name"] = [r.replace(":", "_") for r in data["columns_name"]]
    pyred.send_to_redshift(redshift_instance, data, replace=False, existing_tunnel=existing_tunnel)
    return 0
