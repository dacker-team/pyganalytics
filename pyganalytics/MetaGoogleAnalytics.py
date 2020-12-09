from dbstream import DBStream
from googleauthentication import GoogleAuthentication


class MetaGoogleAnalytics:
    def __init__(self, googleauthentication: GoogleAuthentication, metric_dimension_path, dbstream: DBStream,
                 mapping_path=None,
                 full_schema_name=None):
        self.googleauthentication = googleauthentication
        self.metric_dimension_path = metric_dimension_path
        self.dbstream = dbstream
        self.mapping_path = mapping_path
        self.full_schema_name = full_schema_name
