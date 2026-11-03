"""Nager.Date: expand each long weekend into days and classify them (holiday / weekend / both)."""
from datetime import date

import pandas as pd
import requests

BASE = "https://date.nager.at/api/v3"
YEAR = date.today().year
CODES = ["RO"]


def get_json(path: str):
    r = requests.get(f"{BASE}/{path}", timeout=30)
    r.raise_for_status()
    return r.json()


def classify(is_holiday: bool, is_weekend: bool) -> str:
    if is_holiday and is_weekend:
        return "Public holiday + weekend"
    if is_holiday:
        return "Public holiday"
    if is_weekend:
        return "Weekend"
    return "Bridge day"


def long_weekend_days(code: str) -> pd.DataFrame:
    """One row per day of every long weekend in YEAR, with its holiday name if any."""
    holidays = {h["date"]: h["name"] for h in get_json(f"PublicHolidays/{YEAR}/{code}")}
    rows = []
    for number, lw in enumerate(get_json(f"LongWeekend/{YEAR}/{code}"), start=1):
        for day in pd.date_range(lw["startDate"], lw["endDate"]):
            key = day.strftime("%Y-%m-%d")
            is_holiday = key in holidays
            is_weekend = day.weekday() >= 5
            rows.append({
                "countryCode": code,
                "longWeekend": number,
                "date": key,
                "weekday": day.day_name(),
                "type": classify(is_holiday, is_weekend),
                "holidayName": holidays.get(key),
            })
    return pd.DataFrame(rows)


df = pd.concat([long_weekend_days(code) for code in CODES], ignore_index=True)
print(df.to_string(index=False))
