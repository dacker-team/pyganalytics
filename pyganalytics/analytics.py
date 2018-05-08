import time

import pyspreadsheet
import copy

from .redshift import to_redshift
from .config import get_start_end, get_all_view_id
from pyganalytics.path import get_metric_dimension
from .core import get_data, create_columns_rows
from .date import segment_month_date, segment_ndays_date


def _get_one_segment(project, report, all_view_id, start, end, time_increment, redshift_instance, spreadsheet_id):
    report_name = report.get("name")
    report_config = report.get("config")
    metric = list(report_config["metric"])
    dimension = list(report_config["dimension"])
    metric_filter = report_config.get("metric_filter")
    dimension_filter = report_config.get("dimension_filter")
    output_storage_name = "ga." + report_name + "_" + time_increment.replace(":", "_")

    result = {
        "rows": []
    }
    all_batch_id = []
    print("Loading " + report_name + " " + time_increment + " between " + start + " and " + end)
    for view_id in all_view_id:

        data = get_data(
            project,
            view_id,
            start,
            end,
            metric,
            dimension,
            time_increment,
            metric_filter,
            dimension_filter)

        view_result, view_all_batch_id = create_columns_rows(project, data, view_id, time_increment)
        if result.get("columns_name") is None or (len(view_result["columns_name"]) > len(result["columns_name"])):
            result["columns_name"] = view_result["columns_name"]
        if len(view_result["rows"]) > 0 and len(view_result["rows"][0]) > 2:
            result["rows"] = result["rows"] + view_result["rows"]
        all_batch_id = all_batch_id + view_all_batch_id

    len_result = str(len(result["rows"]))
    print(time_increment + ": " + len_result + " results")

    if redshift_instance:  # Send to Redshift
        result["table_name"] = output_storage_name
        copy_result = copy.deepcopy(result)
        to_redshift(copy_result, all_batch_id, redshift_instance)
        print("Finished sent to Redshift " + report_name + " " + time_increment + " between " + start + " and " + end)
    if spreadsheet_id:  # Prepare to send to spreadsheet
        result["worksheet_name"] = output_storage_name

    return result


def _get_data_by_segment(project, start, end, report, all_view_id, redshift_instance, spreadsheet_id, increment):
    report_name = report.get("name")

    all_time_increment = report.get("config")["time_increment"]
    all_result = []
    for time_increment in all_time_increment:
        if time_increment == 'year':
            result = _get_one_segment(project, report, all_view_id, start, end, time_increment,
                                      redshift_instance, spreadsheet_id)
        else:
            if time_increment == 'day':
                segments = segment_ndays_date(start, end, increment)
            else:
                segments = segment_month_date(start, end)
            i = 0
            for segment in segments:
                segment_data = _get_one_segment(project, report, all_view_id, segment[0], segment[1], time_increment,
                                                redshift_instance, spreadsheet_id)
                if i == 0:  # Concatenate to send to spreadsheet
                    result = segment_data
                    i = i + 1
                else:
                    result["rows"] = result["rows"] + segment_data["rows"]
                time.sleep(2)
        # Send to spreadsheet
        if spreadsheet_id:
            pyspreadsheet.send_to_sheet(project, spreadsheet_id, result)
            print("Finished sent to Spreadsheet " + report_name +
                  " " + time_increment + " between " + start + " and " + end)
        all_result.append(result)
    return all_result


def get(project, test=False, start=None, end=None, all_view_id=None, spreadsheet_id=None, redshift_instance=None,
        increment=5):
    """
    :param test: if test = True --> other params are set up automatically
    :param start: "yyyy-mm-dd"
    :param end: "yyyy-mm-dd"
    :param all_view_id: list of view_id, or "*" to catch data from all allowed views
    :param spreadsheet_id: id of Google Sheets to eventually send
    :param redshift_instance: redshift instance to eventually send (see pyred documentation)
    :return: {
        "":
        "columns_name": []
        "rows": []
    }
    """
    metric_dimension = get_metric_dimension(project, test)
    start, end = get_start_end(start, end)
    all_view_id = get_all_view_id(project, test, all_view_id)

    for report_name in metric_dimension.keys():
        report = {
            "name": report_name,
            "config": metric_dimension[report_name]
        }
        print("Loading report %s" % report_name)
        all_result = _get_data_by_segment(project, start, end, report, all_view_id, redshift_instance, spreadsheet_id,
                                          increment)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None:
            print(all_result)
        time.sleep(5)
