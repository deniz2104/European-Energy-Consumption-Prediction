from requests.auth import AuthBase
from typing import Any
from src.importer.client.retry_session import RetrySession
from src.importer.constants.general import (
    METHOD,
    TIMEOUT
)

class APIClient(AuthBase):
    def _init_(self, base_url : str , token : str | None = None):
        self._base_url = base_url
        self._token = token
        self._session = RetrySession()

    def _call_(self, r):
        if self._token:
            r.headers["Authorization"] = f"Bearer {self._token}"
        
        return r
    
    ## we should work on this query parameters here. use request open source code
    def request(self, endpoint_params: dict[str,Any] | None = None, path_params: dict[str, Any] | None = None, query_params: dict[str, Any] | None = None) -> Any:
        r = self._session.request(
            METHOD,
            self._base_url.format(**((endpoint_params or {}) | (path_params or {}))),
            params=query_params,
            auth=self,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()

    def close(self) -> None:
        self._session.close()

    def _enter_(self):
        return self

    def _exit_(self, *exc) -> None:
        self.close()