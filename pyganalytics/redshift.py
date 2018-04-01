import psycopg2
import pyred


def to_redshift(result, all_batch_id, redshift_instance):
    all_batch_id = ["'" + e + "'" for e in all_batch_id]
    redshift_table = result["table_name"]
    if all_batch_id:
        try:
            query = 'DELETE FROM ' + redshift_table + ' WHERE batch_id IN ' + "(" + ",".join(all_batch_id) + ")"
            pyred.execute.execute_query('MH', query)
        except psycopg2.ProgrammingError:
            pass
    result["columns_name"] = [r.replace(":", "_") for r in result["columns_name"]]
    pyred.send_to_redshift(redshift_instance, result, replace=False)
    return 0