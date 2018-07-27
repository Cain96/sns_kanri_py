import datetime


def date_range(start_date: datetime.date, end_date: datetime.date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + datetime.timedelta(n)
