def get_metrics(response):
    """
    Extract asked metrics from api response
    @list_metrics : list of dict
    """
    list_metrics = []
    for i in response['reports'][0]['columnHeader']['metricHeader']['metricHeaderEntries']:
        list_metrics.append(i['name'])
    return list_metrics


def get_dimensions(response):
    """
      Extract asked dimensions from api response
      @list_dimensions : list of dict
    """
    return response['reports'][0]['columnHeader']['dimensions']


def extract_api_data(response):
    """
    Extract all data from api response
    """
    try:
        rows = response['reports'][0]['data']['rows']
    except:
        return []
    sampling = False
    samples_read_counts = response['reports'][0]['data'].get('samplesReadCounts')
    sampling_space_sizes = response['reports'][0]['data'].get('samplingSpaceSizes')
    if samples_read_counts:
        print("SAMPLING")
        sampling = True

    metric_response = get_metrics(response)
    dimensions_response = get_dimensions(response)
    data = []
    for row in rows:
        d = {}
        j = 0
        for i in dimensions_response:
            d[i] = row['dimensions'][j]
            j = j + 1
        j = 0
        for i in metric_response:
            d[i] = row['metrics'][0]['values'][j]
            j = j + 1
        d["sampling"] = sampling

        data.append(d)
    return data
