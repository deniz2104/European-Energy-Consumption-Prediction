from typing import Final
from src.importer.constants.general import DATA_DIR
from src.importer.source import Column

REST_COUNTRIES_URL : Final[str] = "https://api.restcountries.com/countries/v5/region/Europe"
REST_COUNTRIES_LIMIT : Final[int] = 100
REST_COUNTRIES_PAUSE : Final[int] = 1
REST_COUNTRIES_FILE : Final[str] = str(DATA_DIR / "countries.csv")

REST_COUNTRIES_FIELDS: Final[list[Column]] = [
    Column("names.common", "Name"),
    Column("codes.alpha_2", "Code"),
    Column("subregion", "SubRegion"),
    Column("coordinates.lat", "Latitude"),
    Column("coordinates.lng", "Longitude"),
]