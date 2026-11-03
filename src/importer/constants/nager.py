from typing import Final
from src.importer.constants.general import DATA_DIR

NAGER_URL : Final[str] = "https://date.nager.at/api/v3/{endpoint}/{year}/{code}"
NAGER_PUBLIC_HOLIDAY_ENDPOINT : Final[str] = "PublicHolidays"
NAGER_LONG_WEEKEND_ENDPOINT : Final[str] = "LongWeekend"

NAGER_HOLIDAYS_FILE : Final[str] = str(DATA_DIR / "nager_holidays.csv")
NAGER_LONG_WEEKENDS_FILE : Final[str] = str(DATA_DIR / "nager_long_weekends.csv")

NAGER_HOLIDAY_FIELDS : Final[dict[str, str]] = {
    "date": "Date",
    "localName": "LocalName",
    "name": "Name",
    "global": "Global",          
    "types": "Types",         
}

NAGER_LONG_WEEKEND_FIELDS : Final[dict[str, str]] = {
    "startDate": "StartDate",
    "endDate": "EndDate",
    "dayCount": "DayCount",
    "needBridgeDay": "NeedBridgeDay",
}
