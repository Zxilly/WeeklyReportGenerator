from datetime import datetime

time_template = "%Y-%m-%dT%H:%M:%SZ"


def str2time(s: str):
    return datetime.strptime(s, time_template)


def time2str(t: datetime):
    return datetime.strftime(t, time_template)
