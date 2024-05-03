from datetime import datetime, timedelta


def split_date_range_by_months(from_date, to_date):
    date_range = []
    current_date = from_date
    while current_date <= to_date:
        next_month = current_date.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)
        date_range.append((current_date, min(next_month - timedelta(days=1), to_date)))
        current_date = next_month
    return date_range
