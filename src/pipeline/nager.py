"""Nager.Date pipeline.

Step 1 (this file for now): raw public holidays and long weekends, whole years, every country.

From the project root:
    uv run python -m src.pipeline.nager            # every country in countries.csv
    uv run python -m src.pipeline.nager RO MC XK   # only these codes
"""
import logging
import sys

import pandas as pd

from src.importer.constants.dates import YEARS
from src.importer.constants.nager import (
    NAGER_HOLIDAY_FIELDS,
    NAGER_HOLIDAYS_FILE,
    NAGER_LONG_WEEKEND_ENDPOINT,
    NAGER_LONG_WEEKEND_FIELDS,
    NAGER_LONG_WEEKENDS_FILE,
    NAGER_PUBLIC_HOLIDAY_ENDPOINT,
    NAGER_URL,
)
from src.importer.constants.rest_countries import REST_COUNTRIES_FILE
from src.importer.exporter import collect, write_csv
from src.importer.pagination import SinglePage
from src.importer.source import Source

log = logging.getLogger(__name__)


def load_codes() -> list[str]:
    # keep_default_na=False: a code like "NA" must stay a string, not become a missing value
    return pd.read_csv(REST_COUNTRIES_FILE, keep_default_na=False)["Code"].tolist()


def nager_source(endpoint: str, columns: dict[str, str]) -> Source:
    return Source(
        api_token=None,
        url=NAGER_URL,
        path_params={"endpoint": endpoint},
        query_params=None,
        columns=columns,
        paginator=SinglePage(records_path=""),
    )


def fetch_raw(endpoint: str, columns: dict[str, str], codes: list[str], years: list[int]) -> pd.DataFrame:
    """One call per (code, year); whole years, capping to the date window happens later."""
    base = nager_source(endpoint, columns)
    variants = (
        (base.with_params(path_params={"year": year, "code": code}), {"Code": code, "Year": year})
        for code in codes
        for year in years
    )
    return collect(variants)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    codes = sys.argv[1:] or load_codes()
    log.info("%d countries x years %s", len(codes), YEARS)

    for endpoint, columns, path in (
        (NAGER_PUBLIC_HOLIDAY_ENDPOINT, NAGER_HOLIDAY_FIELDS, NAGER_HOLIDAYS_FILE),
        (NAGER_LONG_WEEKEND_ENDPOINT, NAGER_LONG_WEEKEND_FIELDS, NAGER_LONG_WEEKENDS_FILE),
    ):
        df = fetch_raw(endpoint, columns, codes, YEARS)
        write_csv(df, path)
        log.info("%s: %d rows, %d countries -> %s", endpoint, len(df), df["Code"].nunique() if len(df) else 0, path)


if __name__ == "__main__":
    main()
