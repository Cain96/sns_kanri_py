import datetime
from datetime import datetime as dt


def date_range(start_date: datetime.date, end_date: datetime.date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + datetime.timedelta(n)


def get_total_time(queryset):
    times = queryset.values_list('time', flat=True)
    times = map(lambda time: dt.combine(datetime.date.min, time) - dt.min, times)
    return int(sum(times, datetime.timedelta()).total_seconds())
