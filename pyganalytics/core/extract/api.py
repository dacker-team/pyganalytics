def set_dimensions(dimensions):
    """
    Set properly dimensions that we want to load
    @dimensions: list
    """
    result = []
    for i in dimensions:
        d = {
            'name': i
        }
        result.append(d)
    return result


def set_metrics(metrics):
    """
    Set properly metrics that we want to load
    @metrics: list
    """
    result = []
    for i in metrics:
        d = {
            'expression': i
        }
        result.append(d)
    return result


def set_date_range(start_date, end_date):
    """
    Set properly date range
    @start_date: string date "yyyy-mm-dd"
    @end_date: string date "yyyy-mm-dd"
    """
    return [{'startDate': start_date, 'endDate': end_date}]


def get_report(analytics, view_id, dimensions, metrics, start_date, end_date, sampling_level="LARGE",
               metric_filter=None, dimension_filter=None, segments=None, page_token=None):
    """
    Use the Analytics Service Object to query the Analytics Reporting API V4.
    @analytics: result of initialize_api function
    @view_id: Id of Customer's Google Analytics View
    @dimensions: list of dimensions (set at the top of the script)
    @metrics: list of metrics (set at the top of the script)
    @start_date: string date "yyyy-mm-dd"
    @end_date: string date "yyyy-mm-dd"
    @samplingLevel : samplingLevel, "LARGE" by default

    return : API response
    """
    body = {
        'reportRequests': [
            {
                'viewId': view_id,
                'dateRanges': set_date_range(start_date, end_date),
                'dimensions': set_dimensions(dimensions),
                'metrics': set_metrics(metrics),
                'samplingLevel': sampling_level,
                "pageToken": page_token
            }]
    }
    if metric_filter:
        body["reportRequests"][0]["metricFilterClauses"] = metric_filter
    if dimension_filter:
        body["reportRequests"][0]["dimensionFilterClauses"] = dimension_filter
    if segments:
        body["reportRequests"][0]["segments"] = segments
    response = analytics.reports().batchGet(body=body).execute()
    return response
