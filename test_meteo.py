"""Open-Meteo archive: one year of hourly weather for a country, located by its code."""
import json
import sys
from typing import Final

import pandas as pd
import requests

OPEN_METEO: Final[str] = "https://archive-api.open-meteo.com/v1/archive"
YEAR = 2025
CODES = sys.argv[1:] or ["RO"]
HOURLY: Final[list[str]] = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "cloud_cover",
    "wind_speed_10m",
    "shortwave_radiation",
]

with open("europe_countries.json", encoding="utf-8") as f:
    countries = pd.DataFrame(json.load(f)).set_index("Code")


def year_weather(code: str) -> pd.DataFrame:
    """Hourly weather for YEAR at the country's coordinates."""
    country = countries.loc[code]
    r = requests.get(
        OPEN_METEO,
        params={
            "latitude": country["Latitude"],
            "longitude": country["Longitude"],
            "start_date": f"{YEAR}-01-01",
            "end_date": f"{YEAR}-12-31",
            "hourly": ",".join(HOURLY),
            "timezone": "auto",
        },
        timeout=60,
    )
    r.raise_for_status()
    weather = pd.DataFrame(r.json()["hourly"]).rename(columns={"time": "datetime"})
    weather["datetime"] = pd.to_datetime(weather["datetime"])
    weather.insert(0, "countryCode", code)
    return weather


df = pd.concat([year_weather(code) for code in CODES], ignore_index=True)
print(df.head(10).to_string(index=False))
print(f"\n{len(df)} rows, {df['datetime'].min()} to {df['datetime'].max()}")
print(df.isna().sum().to_string())
