import time

import pyspreadsheet

from .redshift import to_redshift
from .config import get_start_end, get_metric_dimension, get_all_view_id
from .core import get_data, create_columns_rows
from .date import segment_month_date


def _get_one_segment(report, view_id, start, end, time_increment, redshift_instance, spreadsheet_id):
    report_name = report.get("name")
    report = report.get("config")
    metric = list(report["metric"])
    dimension = list(report["dimension"])
    metric_filter = report.get("metric_filter")
    dimension_filter = report.get("dimension_filter")

    print("Loading " + report_name + " " + time_increment + " between " + start + " and " + end)
    data = get_data(
        view_id,
        start,
        end,
        metric,
        dimension,
        time_increment,
        metric_filter,
        dimension_filter)
    output_storage_name = "ga." + report_name + "_" + time_increment
    result, all_batch_id = create_columns_rows(data, view_id, time_increment)
    len_result = str(len(result["rows"]))
    print(time_increment + ": " + len_result + " results")

    if redshift_instance:  # Send to Redshift
        result["table_name"] = output_storage_name
        to_redshift(result, all_batch_id, redshift_instance)
        print("Finished sent to Redshift " + report_name + " " + time_increment + " between " + start + " and " + end)
    if spreadsheet_id:  # Prepare to send to spreadsheet
        result["worksheet_name"] = output_storage_name

    return result


def _get_data_by_segment(start, end, report, view_id, spreadsheet_id, redshift_instance):
    report_name = report.get("name")
    report = report.get("config")
    all_time_increment = report["time_increment"]
    all_result = []
    for time_increment in all_time_increment:
        if time_increment == 'year':
            result = _get_one_segment(report, view_id, start, end, time_increment, spreadsheet_id, redshift_instance)
        else:
            segments = segment_month_date(start, end)
            i = 0
            for segment in segments:
                segment_data = _get_one_segment(report, view_id, segment[0], segment[1], time_increment, spreadsheet_id,
                                                redshift_instance)
                if i == 0:  # Concatenate to send to spreadsheet
                    result = segment_data
                    i = i + 1
                else:
                    result["rows"] = result["rows"] + segment_data["rows"]
                time.sleep(2)
        # Send to spreadsheet
        if spreadsheet_id:
            pyspreadsheet.send_to_sheet(spreadsheet_id, result)
            print("Finished sent to Spreadsheet " + report_name +
                  " " + time_increment + " between " + start + " and " + end)
        all_result.append(result)
    return all_result


def get(test=False, start=None, end=None, all_view_id=None, spreadsheet_id=None, redshift_instance=None):
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
    metric_dimension = get_metric_dimension(test)
    start, end = get_start_end(start, end)
    all_view_id = get_all_view_id(test, all_view_id)
    for view_id in all_view_id:
        for report_name in metric_dimension.keys():
            report = {
                "name": report_name,
                "config": metric_dimension[report_name]
            }
            print("Loading report %s of view %s" % (report_name, view_id))
            all_result = _get_data_by_segment(start, end, report, view_id, spreadsheet_id, redshift_instance)
            print("Finish loading report %s of view %s" % (report_name, view_id))
            if spreadsheet_id is None and redshift_instance is None:
                print(all_result)
            time.sleep(5)
