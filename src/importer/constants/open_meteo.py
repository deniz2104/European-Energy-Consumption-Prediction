from typing import Final
from src.importer.source import Column

OPEN_METEO_URL : Final[str] = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_TIMEZONE : Final[str] = "auto"

OPEN_METEO_FIELDS : Final[list[Column]] = [
    Column("time", "Datetime"),
    Column("temperature_2m", "Temperature"),
    Column("relative_humidity_2m", "Humidity"),
    Column("precipitation", "Precipitation"),
    Column("cloud_cover", "Cloud Cover"),
    Column("wind_speed_10m", "Wind Speed"),
    Column("shortwave_radiation", "Shortwave Radiation"),
]