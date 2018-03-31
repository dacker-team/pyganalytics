def construct_range(worksheet_name, start, end=None):
    range = "'" + worksheet_name + "'" + "!" + start
    if end:
        range = range + ":" + end
    return range


def column_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string