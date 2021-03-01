import copy
from pyganalytics import MetaGoogleAnalytics
from pyganalytics.core.extract.api import get_report
from pyganalytics.core.transform.extract import extract_api_data
from pyganalytics.core.transform.path import mapping_path
import hashlib
from isoweek import Week


def create_id(view_id, date):
    a = str(view_id) + str(date)
    id_batch = hashlib.sha224(a.encode()).hexdigest()
    return id_batch


def treat_data(data, metric, dimension):
    """
    Treat Data:
    -Cluster sources
    -Date and metric format
    """
    for i in data:
        for d in dimension:
            if d == "ga:yearMonth":
                i["date"] = i[d][:4] + "-" + i[d][-2:] + "-01"
            elif d == "ga:year":
                i["date"] = i[d] + "-01-01"
            elif d == "ga:isoYearIsoWeek":
                week = Week(int(i[d][:4]), int(i[d][-2:])).monday()
                i["date"] = str(week)[:10]
            elif d == "ga:date":
                i["date"] = i[d][:4] + "-" + i[d][4:6] + "-" + i[d][6:8]
            if len(i[d]) > 254:
                i[d] = i[d][:254]
    return data


def get_data(googleanalytics: MetaGoogleAnalytics, view_id, start, end, metric, dimension, time_increment,
             metric_filter=None,
             dimension_filter=None, segment=None):
    print(view_id)
    dimension = copy.deepcopy(dimension)
    dimension.append(time_increment)
    analytics = googleanalytics.googleauthentication.get_account("analyticsreporting")

    if metric_filter is not None:
        metric_filter = [
            {
                "filters": metric_filter
            }]
    if dimension_filter is not None:
        dimension_filter = [
            {
                "filters": dimension_filter
            }
        ]
    if segment:
        segment = [{"segmentId": segment}]

    response = get_report(analytics, view_id, dimension, metric, start, end, metric_filter=metric_filter,
                          dimension_filter=dimension_filter, segments=segment)

    next_page_token = response['reports'][0].get("nextPageToken")

    api_data, types = extract_api_data(response)
    data = treat_data(api_data, metric, dimension)

    while next_page_token is not None:
        response = get_report(analytics, view_id, dimension, metric, start, end, metric_filter=metric_filter,
                              dimension_filter=dimension_filter, segments=segment, page_token=next_page_token)

        next_page_token = response['reports'][0].get("nextPageToken")

        api_data, types = extract_api_data(response)
        data = data + treat_data(api_data, metric, dimension)
    return data, types


def create_columns_rows(data, view_id, time_increment, types):
    try:
        column_name = list(data[0].keys())
    except IndexError:
        column_name = []
    rows = []
    all_batch_id = []
    for element in data:
        row = []
        batch_id = create_id(view_id, element[time_increment])
        for c in column_name:
            row.append(element[c])

        row.append(view_id)
        row.append(batch_id)
        rows.append(row)
        if batch_id not in all_batch_id:
            all_batch_id.append(batch_id)
    column_name.append("view_id")
    column_name.append("batch_id")
    result = {
        "columns_name": column_name,
        "rows": rows,
        "types": types
    }
    return result, all_batch_id
