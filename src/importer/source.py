from dataclasses import dataclass
from typing import Any, Iterable, Iterator, Protocol
from itertools import product

from src.importer.client.api_client import APIClient

class Paginator(Protocol):
    def pages(self, api: APIClient, endpoint_params: dict | None, path_params: dict | None, query_params: dict | None) -> Iterable[Any]: ...

@dataclass(frozen=True)
class Source:
    api_token: str | None
    url: str
    endpoint_params: dict[str, Any] | None
    path_keys: list[str] | None
    path_values: list[list[Any]] | None
    query_params: dict[str, Any] | None
    columns: dict[str, str]
    paginator: Paginator

    def __post_init__(self):
        if len(self.path_keys or []) != len(self.path_values or []):
            raise ValueError(
                f"path_keys ({len(self.path_keys or [])}) and path_values ({len(self.path_values or [])}) must have the same length"
            )

    @property
    def path_params(self) -> list[dict[str, Any]]:
        return [dict(zip(self.path_keys or [], combo)) for combo in product(*self.path_values)] if self.path_values else [{}]

    def fetch(self) -> Iterator[Any]:
        with APIClient(self.url, self.api_token) as api:
            for path in self.path_params:
                yield from self.paginator.pages(api, self.endpoint_params or {}, path, self.query_params or {})
