import json
import yaml
from pyganalytics.mapping import mapping


def mapping_path(googleanalytics):
    google_analytics_mapping_path = googleanalytics.mapping_path
    if google_analytics_mapping_path:
        custom_mapping = open(google_analytics_mapping_path).read()
        custom_mapping = json.loads(custom_mapping)
        mapping.update(custom_mapping)
    mapping_reverse = {}
    for x in mapping.keys():
        mapping_reverse[mapping[x]] = x
    return mapping, mapping_reverse


def get_metric_dimension(googleanalytics):
    try:
        return yaml.load(open(googleanalytics.metric_dimension_path), Loader=yaml.FullLoader)
    except Exception as e:
        print("Error with metric_dimension_file : %s" % str(e))
        exit()
