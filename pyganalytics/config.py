import datetime
import os

import yaml

import pyganalytics
from pyganalytics.manage_view import get_all_access_view
from .date import remove_a_month


def get_metric_dimension(test):
    google_analytics_yaml_path = os.environ.get("GOOGLE_ANALYTICS_YAML_PATH")
    if test and not google_analytics_yaml_path:
        google_analytics_yaml_path = os.path.join(os.path.dirname(pyganalytics.__file__), "config.yaml")
    elif not google_analytics_yaml_path:
        print("No GOOGLE_ANALYTICS_YAML_PATH configured")
        exit()
    with open(google_analytics_yaml_path, 'r') as stream:
        metric_dimension = yaml.load(stream)
    return metric_dimension


def get_start_end(start, end):
    if not end:
        end = str(datetime.datetime.now())[:10]
    if not start:
        start = str(datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=-10))[:10]
    return start, end


def get_all_view_id(test, all_view_id):
    if (not all_view_id) and test:
        all_view_id = get_all_access_view()
        all_view_id = [ai["view_id"] for ai in all_view_id][:1]
    elif all_view_id == "*":
        all_view_id = get_all_access_view()
        all_view_id = [ai["view_id"] for ai in all_view_id]
    elif not all_view_id:
        print("No list of view_id given as argument")
        exit()
    return all_view_id
