import requests
from requests.adapters import HTTPAdapter
from src.importer.client.retry import RETRY_POLICY

class RetrySession(requests.Session):
    def __init__(self):
        super().__init__()
        adapter = HTTPAdapter(max_retries=RETRY_POLICY)
        self.mount("https://", adapter)
        self.mount("http://", adapter)