from requests.auth import AuthBase
from typing import Any
from src.importer.client.retry_session import RetrySession
from src.importer.constants.general import (
    METHOD,
    TIMEOUT
)

class APIClient(AuthBase):
    def __init__(self, base_url : str , token : str | None = None):
        self._base_url = base_url
        self._token = token
        self._session = RetrySession()

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self._token}" if self._token else ""
        return r

    def request(self, path_params: dict[str, Any] | None = None, query_params: dict[str, Any] | None = None) -> Any:
        r = self._session.request(
            METHOD,
            self._base_url.format(**(path_params or {})),
            params=query_params,
            auth=self,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()

    def close(self) -> None:
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> None:
        self.close()