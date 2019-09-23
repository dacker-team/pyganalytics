import time
import copy

from pyganalytics.MetaGoogleAnalytics import MetaGoogleAnalytics
from pyganalytics.core.load.to_database import send_to_db
from pyganalytics.core.extract.config import get_start_end, get_all_view_id
from pyganalytics.core.transform.path import get_metric_dimension
from pyganalytics.core.transform.core import get_data, create_columns_rows
from pyganalytics.core.extract.date import segment_month_date, segment_ndays_date


def _get_one_segment(googleanalytics, report, all_view_id, start, end, time_increment, prefix_schema):
    report_name = report.get("name")
    report_config = report.get("config")
    metric = list(report_config["metric"])
    dimension = list(report_config["dimension"])
    metric_filter = report_config.get("metric_filter")
    dimension_filter = report_config.get("dimension_filter")
    segment = report_config.get("segment")
    output_storage_name = "ga." + report_name + "_" + time_increment.replace(":", "_")
    if prefix_schema:
        output_storage_name = prefix_schema + "_" + output_storage_name

    result = {
        "rows": []
    }
    all_batch_id = []
    print("Loading " + report_name + " " + time_increment + " between " + start + " and " + end)
    for view_id in all_view_id:

        data = get_data(
            googleanalytics,
            view_id,
            start,
            end,
            metric,
            dimension,
            time_increment,
            metric_filter,
            dimension_filter,
            segment)

        view_result, view_all_batch_id = create_columns_rows(googleanalytics, data, view_id, time_increment)
        if result.get("columns_name") is None or (len(view_result["columns_name"]) > len(result["columns_name"])):
            result["columns_name"] = view_result["columns_name"]
        if len(view_result["rows"]) > 0 and len(view_result["rows"][0]) > 2:
            result["rows"] = result["rows"] + view_result["rows"]
        all_batch_id = all_batch_id + view_all_batch_id

    len_result = str(len(result["rows"]))
    print(time_increment + ": " + len_result + " results")

    result["table_name"] = output_storage_name
    copy_result = copy.deepcopy(result)
    send_to_db(dbstream=googleanalytics.dbstream, data=copy_result, all_batch_id=all_batch_id)
    print("Finished sent to Database " + report_name + " " + time_increment + " between " + start + " and " + end)

    return result


def _get_data_by_segment(googleanalytics, start, end, report, all_view_id, increment, prefix_schema):
    all_time_increment = report.get("config")["time_increment"]
    all_result = []
    for time_increment in all_time_increment:
        if time_increment == 'year':
            result = _get_one_segment(googleanalytics, report, all_view_id, start, end, time_increment, prefix_schema)
        else:
            if time_increment == 'day':
                segments = segment_ndays_date(start, end, increment)
            else:
                segments = segment_month_date(start, end)
            i = 0
            for segment in segments:
                segment_data = _get_one_segment(googleanalytics, report, all_view_id, segment[0], segment[1],
                                                time_increment, prefix_schema)
                if i == 0:  # Concatenate to send to spreadsheet
                    result = segment_data
                    i = i + 1
                else:
                    result["rows"] = result["rows"] + segment_data["rows"]
                time.sleep(2)
        all_result.append(result)
    return all_result


class GoogleAnalytics(MetaGoogleAnalytics):

    def get(self,
            start=None,
            end=None,
            all_view_id=None,
            prefix_schema=None,
            increment=5,
            return_result=False):
        metric_dimension = get_metric_dimension(self)
        start, end = get_start_end(start, end)
        all_view_id = get_all_view_id(self, all_view_id)

        for report_name in metric_dimension.keys():
            report = {
                "name": report_name,
                "config": metric_dimension[report_name]
            }
            print("Loading report %s" % report_name)
            all_result = _get_data_by_segment(self,
                                              start,
                                              end,
                                              report,
                                              all_view_id,
                                              increment,
                                              prefix_schema,
                                              )
            print("Finish loading report %s" % report_name)
            # time.sleep(5)
            if return_result:
                return all_result