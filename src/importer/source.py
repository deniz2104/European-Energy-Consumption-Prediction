from dataclasses import dataclass, replace
from typing import Any, Iterable, Iterator, Protocol
from src.importer.client.api_client import APIClient

class Paginator(Protocol):
    def pages(self, api: APIClient, path_params: dict | None, query_params: dict) -> Iterable[Any]: ...

@dataclass(frozen=True)
class Source:
    api_token: str | None
    url: str
    path_params: dict[str, Any] | None
    query_params: dict[str, Any] | None
    columns : dict[str,str]
    paginator : Paginator

    def fetch(self) -> Iterator[Any]:
        """Yield the records of each page."""
        with APIClient(self.url, self.api_token) as api:
            yield from self.paginator.pages(api, self.path_params, self.query_params or {})

    def with_params(self, path_params: dict[str, Any] | None = None,
                    query_params: dict[str, Any] | None = None) -> "Source":
        return replace(
            self,
            path_params={**(self.path_params or {}), **(path_params or {})},
            query_params={**(self.query_params or {}), **(query_params or {})},
        )
