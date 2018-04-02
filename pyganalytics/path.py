import json
import os

import yaml

from .metric_dim_example import metric_dimension_example
from .mapping import mapping


def mapping_path(project):
    google_analytics_mapping_path = os.environ.get("GOOGLE_ANALYTICS_%s_MAPPING_PATH" % project)
    if google_analytics_mapping_path:
        custom_mapping = open(google_analytics_mapping_path).read()
        custom_mapping = json.loads(custom_mapping)
        mapping.update(custom_mapping)
    mapping_reverse = {}
    for x in mapping.keys():
        mapping_reverse[mapping[x]] = x
    return mapping, mapping_reverse


def get_metric_dimension(project, test):
    google_analytics_yaml_path = os.environ.get("GOOGLE_ANALYTICS_%s_YAML_PATH" % project)
    if test and not google_analytics_yaml_path:
        return metric_dimension_example
    elif not google_analytics_yaml_path:
        print("No GOOGLE_ANALYTICS_YAML_PATH configured")
        exit()
    with open(google_analytics_yaml_path, 'r') as stream:
        metric_dimension = yaml.load(stream)
    return metric_dimension


def credential_path(project):
    google_client_secret_path = os.environ.get("GOOGLE_%s_CLIENT_SECRET_PATH" % project)
    google_credentials_path = os.environ.get("GOOGLE_%s_CREDENTIALS_PATH" % project)

    if not google_client_secret_path:
        google_client_secret_path = './'

    if not google_credentials_path:
        google_credentials_path = './'

    if google_client_secret_path[-1] == '/':
        google_client_secret_path = google_client_secret_path[:-1]

    if google_credentials_path[-1] == '/':
        google_credentials_path = google_credentials_path[:-1]

    google_client_secret_path = google_client_secret_path + '/client_secrets.json'
    return google_client_secret_path, google_credentials_path
