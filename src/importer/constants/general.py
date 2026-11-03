from typing import Final
from pathlib import Path

METHOD : Final[str] = "GET"
TIMEOUT : Final[int] = 60
RETRY_TOTAL : Final[int] = 3
RETRY_BACKOFF_FACTOR : Final[float] = 0.5
RETRY_STATUS_CODES : Final[tuple[int, ...]] = (429, 502, 503, 504)
DATA_DIR : Final[Path] = Path(__file__).resolve().parents[3] / "data" / "raw"
