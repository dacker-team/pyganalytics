from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"


def date_to_string(date):
    return date.strftime(DATE_FORMAT)


def string_to_date(string):
    return datetime.strptime(string, DATE_FORMAT)


def segment_month_date(start, end):
    """
    start : YYYY-MM-DD
    end : YYYY-MM-DD
    """
    start_datetime = string_to_date(start)
    end_datetime = string_to_date(end)
    result = []

    while start_datetime.replace(day=1) != end_datetime.replace(day=1):
        inter = [date_to_string(start_datetime), date_to_string(end_of_month(start_datetime))]
        result.append(inter)
        start_datetime = add_a_month(start_datetime)
    result.append([date_to_string(start_datetime), date_to_string(end_datetime)])
    return result


def segment_ndays_date(start, end, increment):
    """
    start : YYYY-MM-DD
    end : YYYY-MM-DD
    """
    start_datetime = string_to_date(start)
    end_datetime = string_to_date(end)
    result = []

    while (start_datetime + timedelta(days=increment)) < end_datetime:
        inter = [date_to_string(start_datetime), date_to_string(start_datetime + timedelta(days=increment))]
        result.append(inter)
        start_datetime = start_datetime + timedelta(days=increment + 1)
    result.append([date_to_string(start_datetime), date_to_string(end_datetime)])
    return result


def segment_week_date(start, end, increment):
    """
        start : YYYY-MM-DD
        end : YYYY-MM-DD
        """
    """
       start : YYYY-MM-DD
       end : YYYY-MM-DD
       """
    start_datetime = string_to_date(start)
    end_datetime = string_to_date(end)
    result = []

    start_datetime = start_datetime - timedelta(days=start_datetime.weekday())
    end_datetime = end_datetime - timedelta(days=end_datetime.weekday()) + timedelta(days=6)

    while start_datetime != end_datetime + timedelta(days=1) and start_datetime <= datetime.today():
        inter = [date_to_string(start_datetime),
                 date_to_string(start_datetime + timedelta(days=6))]
        result.append(inter)
        start_datetime = start_datetime + timedelta(days=7)
    return result


def add_a_month(date):
    try:
        next_month = date.replace(month=date.month + 1, day=1)
    except ValueError:
        if date.month == 12:
            next_month = date.replace(year=date.year + 1, month=1, day=1)
        else:
            # next month is too short to have "same date"
            # pick your own heuristic, or re-raise the exception:
            raise
    return next_month


def remove_a_month(date):
    try:
        previous_month = date.replace(month=date.month - 1, day=1)
    except ValueError:
        if date.month == 1:
            previous_month = date.replace(year=date.year - 1, month=12, day=1)
        else:
            # next month is too short to have "same date"
            # pick your own heuristic, or re-raise the exception:
            raise
    return previous_month


def end_of_month(date):
    return add_a_month(date) + timedelta(days=-1)
