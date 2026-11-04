from typing import Final
from src.importer.constants.general import DATA_DIR
from src.importer.source import Column

NAGER_URL : Final[str] = "https://date.nager.at/api/v3/{endpoint}/{year}/{code}"
NAGER_PUBLIC_HOLIDAY_ENDPOINT : Final[str] = "PublicHolidays"
NAGER_LONG_WEEKEND_ENDPOINT : Final[str] = "LongWeekend"

NAGER_HOLIDAYS_FILE : Final[str] = str(DATA_DIR / "nager_holidays.csv")
NAGER_LONG_WEEKENDS_FILE : Final[str] = str(DATA_DIR / "nager_long_weekends.csv")

NAGER_HOLIDAY_FIELDS : Final[list[Column]] = [
    Column("date", "Date"),
    Column("localName", "LocalName"),
    Column("name", "Name"),
    Column("global", "Global"),
    Column("types", "Types"),
]

NAGER_LONG_WEEKEND_FIELDS : Final[list[Column]] = [
    Column("startDate", "StartDate"),
    Column("endDate", "EndDate"),
    Column("dayCount", "DayCount"),
    Column("needBridgeDay", "NeedBridgeDay"),
]