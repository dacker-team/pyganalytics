import datetime
import random
import time
import copy

from dateutil.relativedelta import relativedelta, MO
from googleapiclient.errors import HttpError

from pyganalytics.MetaGoogleAnalytics import MetaGoogleAnalytics
from pyganalytics.core.load.to_database import send_to_db, def_table_name
from pyganalytics.core.extract.config import get_start_end, get_all_view_id
from pyganalytics.core.transform.path import get_metric_dimension
from pyganalytics.core.transform.core import get_data, create_columns_rows
from pyganalytics.core.extract.date import segment_month_date, segment_ndays_date, segment_week_date


def _get_one_segment(googleanalytics, report, all_view_id, start, end, time_increment, prefix_schema):
    report_name = report.get("name")
    report_config = report.get("config")
    metric = list(report_config["metric"])
    dimension = list(report_config["dimension"])
    metric_filter = report_config.get("metric_filter")
    dimension_filter = report_config.get("dimension_filter")
    segment = report_config.get("segment")
    output_storage_name = def_table_name(
        prefix_schema=prefix_schema,
        report_name=report_name,
        time_increment=time_increment,
        googleanalytics=googleanalytics
    )

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


def _get_data_by_segment(googleanalytics, start, end, report, all_view_id, increment, prefix_schema,
                         force_time_increment):
    all_time_increment = report.get("config")["time_increment"]
    if force_time_increment:
        all_time_increment = [force_time_increment]
    all_result = []
    for time_increment in all_time_increment:
        table_name = def_table_name(
            prefix_schema=prefix_schema,
            report_name=report.get("name"),
            time_increment=time_increment,
            googleanalytics=googleanalytics
        )
        start, end = get_start_end(start=start, end=end, table_name=table_name, dbstream=googleanalytics.dbstream)

        if time_increment == 'year':
            result = _get_one_segment(googleanalytics, report, all_view_id, start[:4] + "-01-01", end, time_increment,
                                      prefix_schema)
        else:
            if time_increment == 'day':
                segments = segment_ndays_date(start, end, increment)
            elif time_increment == "week":
                week_start = datetime.datetime.strptime(start, "%Y-%m-%d") + relativedelta(weekday=MO(-1))
                segments = segment_week_date(week_start.strftime("%Y-%m-%d"), end, increment)
            else:
                segments = segment_month_date(start[:7] + "-01", end)
            i = 0
            for segment in segments:
                for n in range(0, 5):
                    try:
                        segment_data = _get_one_segment(googleanalytics, report, all_view_id, segment[0], segment[1],
                                                        time_increment, prefix_schema)
                        break
                    except HttpError as error:
                        if error.resp.reason in ["internalServerError", "backendError"]:
                            time.sleep((2 ** n) + random.random())
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
            return_result=False,
            force_report=None,
            force_time_increment=None):
        metric_dimension = get_metric_dimension(self)
        all_view_id = get_all_view_id(self, all_view_id)
        all_reports = metric_dimension.keys()
        if force_report:
            all_reports = [force_report]
        for report_name in all_reports:
            report = {
                "name": report_name,
                "config": metric_dimension[report_name]
            }
            print("Loading report %s" % report_name)
            all_result = _get_data_by_segment(self,
                                              start=start,
                                              end=end,
                                              report=report,
                                              all_view_id=all_view_id,
                                              increment=increment,
                                              prefix_schema=prefix_schema,
                                              force_time_increment=force_time_increment
                                              )
            print("Finish loading report %s" % report_name)
            # time.sleep(5)
            if return_result:
                return all_result
