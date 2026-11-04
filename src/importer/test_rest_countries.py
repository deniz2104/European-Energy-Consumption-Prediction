from src.importer.constants.rest_countries import (
    REST_COUNTRIES_FIELDS,
    REST_COUNTRIES_FILE,
    REST_COUNTRIES_LIMIT,
    REST_COUNTRIES_PAUSE,
    REST_COUNTRIES_URL,
)
from src.importer.exporter import CsvExporter
from src.importer.pagination import OffsetPagination
from src.importer.source import Source

def rest_countries_source(token: str | None) -> Source:
    return Source(
        api_token=token,
        url=REST_COUNTRIES_URL,
        endpoint_params=None,
        path_keys=None,
        path_values=None,
        query_params=None,
        columns=REST_COUNTRIES_FIELDS,
        paginator=OffsetPagination(
            REST_COUNTRIES_LIMIT, REST_COUNTRIES_PAUSE, records_path="data.objects", more="data.meta.more"
        ),
    )

def main() -> None:
    source = rest_countries_source("rc_live_f4a2bb3a38b143108bca415889ed9d08")
    df = CsvExporter(source).to_frame()
    CsvExporter.export(df, REST_COUNTRIES_FILE)


if __name__ == "__main__":
    main()