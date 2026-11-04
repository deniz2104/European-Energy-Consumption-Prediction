import logging
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from src.importer.source import Source

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class CsvExporter:
    def _init_(self, source: Source):
        self.source = source

    @staticmethod
    def export(df: pd.DataFrame, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8")

    def to_frame(self) -> pd.DataFrame:
        df = self._pages_to_dataframe(self.source.fetch())
        fields, names = zip(*self.source.columns)
        df = df.reindex(columns=list(fields)).set_axis(list(names), axis=1)
        return self._drop_incomplete_rows(df)

    @staticmethod
    def _pages_to_dataframe(pages: Iterable[list[dict[str, Any]]]) -> pd.DataFrame:
        frames = [pd.json_normalize(page) for page in pages if page]
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    @staticmethod
    def _drop_incomplete_rows(df: pd.DataFrame) -> pd.DataFrame:
        incomplete = (df.isna() | df.eq("")).any(axis=1)
        if incomplete.any():
            log.warning("dropped %d/%d rows with a null/empty value", incomplete.sum(), len(df))
        return df[~incomplete].reset_index(drop=True)