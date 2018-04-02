metric_dimension_example = {
    'traffic': {
        'metric': [
            'ga:sessions',
            'ga:users',
            'ga:pageviews',
            'ga:avgSessionDuration',
            'ga:percentNewSessions',
            'ga:bounces'
        ],
        'dimension': [
            'ga:country'
        ],
        'metric_filter': {
            'metricName': 'ga:users',
            'operator': 'GREATER_THAN',
            'comparisonValue': '100'
        },
        'time_increment': [
            'week',
            'day'
        ]
    }
}
