import time
from typing import Any

from src.importer.client.api_client import APIClient

def _dig_json(data: Any, path: str) -> Any:
    for key in filter(None, path.split(".")):
        data = data[key]
    return data

class SinglePage:
    def __init__(self, records_path: str):
        self.records_path = records_path

    def pages(self, api: APIClient, endpoint_params: dict | None,  path_params: dict | None, query_params: dict | None):
        raw = api.request(endpoint_params, path_params, query_params)
        yield _dig_json(raw, self.records_path)

class OffsetPagination:
    START_OFFSET = 0

    def __init__(self, limit: int, pause: float, records_path: str, more: str):
        self.limit, self.pause, self.records_path, self.more = limit, pause, records_path, more

    def pages(self, api: APIClient, endpoint_params: dict | None, path_params: dict | None, query_params: dict | None):
        while True:
            raw = api.request(
                endpoint_params,
                path_params,
                query_params={**(query_params or {}), "limit": self.limit, "offset": self.START_OFFSET},
            )
            records = _dig_json(raw, self.records_path)
            yield records
            if not _dig_json(raw, self.more) or not records:
                return
            self.START_OFFSET += len(records)
            time.sleep(self.pause)