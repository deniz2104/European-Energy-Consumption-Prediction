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

    def pages(self, api: APIClient, path_params: dict | None, query_params: dict):
        raw = api.request(path_params=path_params, query_params=query_params)
        yield _dig_json(raw, self.records_path)


class OffsetPagination:
    def __init__(self, limit: int, pause: float, records_path: str, more: str):
        self.limit, self.pause, self.records_path, self.more = limit, pause, records_path, more

    def pages(self, api: APIClient, path_params: dict | None, query_params: dict):
        offset = 0
        while True:
            raw = api.request(
                path_params=path_params,
                query_params={**query_params, "limit": self.limit, "offset": offset},
            )
            records = _dig_json(raw, self.records_path)
            yield records
            if not _dig_json(raw, self.more) or not records:
                return
            offset += len(records)
            time.sleep(self.pause)
