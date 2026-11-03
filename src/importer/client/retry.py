from urllib3.util import Retry
from src.importer.constants.general import (
    RETRY_TOTAL,
    RETRY_BACKOFF_FACTOR,
    RETRY_STATUS_CODES
)

RETRY_POLICY = Retry(
    total=RETRY_TOTAL,
    backoff_factor=RETRY_BACKOFF_FACTOR,
    status_forcelist=RETRY_STATUS_CODES
)