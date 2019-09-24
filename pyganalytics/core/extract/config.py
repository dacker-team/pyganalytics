import datetime
from pyganalytics.core.extract.manage_view import get_all_access_view


def get_start_end(start, end):
    if not end:
        end = str(datetime.datetime.now())[:10]
    if not start:
        start = str(datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=-10))[:10]
    return start, end


def get_all_view_id(googleanalytics, all_view_id):
    if all_view_id == "*":
        all_view_id = get_all_access_view(googleanalytics)
        all_view_id = [ai["view_id"] for ai in all_view_id]
    elif not all_view_id:
        print("No list of view_id given as argument")
        exit()
    return all_view_id
