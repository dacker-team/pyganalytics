import datetime

from dbstream import DBStream

from pyganalytics.core.extract.manage_view import get_all_access_view


def get_start_end(start, end, table_name, dbstream: DBStream):
    if not end:
        end = str(datetime.datetime.now())[:10]
    if not start:
        schema_name = table_name.split(".")[0]
        table_name = table_name.split(".")[1]
        max_date = dbstream.get_max(schema=schema_name, table=table_name, field="date", filter_clause="")
        if not max_date:
            start = str(datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=-10))[:10]
        else:
            if isinstance(max_date, str):
                max_date = datetime.datetime.strptime(max_date, "%Y-%m-%d")
            start = str(
                max_date +
                datetime.timedelta(days=-1)
            )[:10]
    return start, end


def get_all_view_id(googleanalytics, all_view_id):
    if all_view_id == "*":
        all_view_id = get_all_access_view(googleanalytics)
        all_view_id = [ai["view_id"] for ai in all_view_id]
    elif not all_view_id:
        print("No list of view_id given as argument")
        exit()
    return all_view_id
