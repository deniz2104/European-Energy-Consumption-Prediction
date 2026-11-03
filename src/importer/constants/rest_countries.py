from typing import Final
from src.importer.constants.general import DATA_DIR

REST_COUNTRIES_URL : Final[str] = "https://api.restcountries.com/countries/v5/region/Europe"
REST_COUNTRIES_LIMIT : Final[int] = 100
REST_COUNTRIES_PAUSE : Final[int] = 1
REST_COUNTRIES_FILE : Final[str] = str(DATA_DIR / "countries.csv")

REST_COUNTRIES_FIELDS: Final[dict[str, str]] = {
    "names.common": "Name",
    "codes.alpha_2": "Code",
    "subregion": "SubRegion",
    "coordinates.lat": "Latitude",
    "coordinates.lng": "Longitude",
}
