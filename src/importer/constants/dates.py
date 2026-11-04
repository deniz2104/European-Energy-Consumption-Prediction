import pandas as pd

LAG_DAYS = 5
HISTORY_YEARS = 3

def end_date() -> str:
    return (pd.Timestamp.today().normalize() - pd.Timedelta(days=LAG_DAYS)).date().isoformat()

def start_date() -> str:
    return (pd.Timestamp(end_date()) - pd.DateOffset(years=HISTORY_YEARS)).date().isoformat()

def years() -> list[int]:
    return list(range(pd.Timestamp(start_date()).year, pd.Timestamp(end_date()).year + 1))