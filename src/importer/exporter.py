import logging
import pandas as pd
import requests
from pathlib import Path
from typing import Any, Iterable
from src.importer.source import Source

log = logging.getLogger(__name__)

class CsvExporter:
    def __init__(self, source: Source):
        self.source = source

    def export(self, path: str | Path) -> None:
        write_csv(self.to_frame(), path)

    def to_frame(self) -> pd.DataFrame:
        df = self._records_to_dataframe(self.source.fetch())
        if df.empty:
            return pd.DataFrame(columns=list(self.source.columns.values()))
        
        df = self._select_columns(df, self.source.columns)
        return self._drop_incomplete_rows(df)

    @staticmethod
    def _records_to_dataframe(pages: Iterable[Any]) -> pd.DataFrame:
        page = [pd.DataFrame(record) if isinstance(record, dict) else pd.json_normalize(record) for record in pages]
        return pd.concat(page, ignore_index=True)

    @staticmethod
    def _select_columns(df: pd.DataFrame, columns: dict[str, str]) -> pd.DataFrame:
        wanted_columns = list(columns)
        return df[wanted_columns].rename(columns=columns)

    @staticmethod
    def _drop_incomplete_rows(df: pd.DataFrame) -> pd.DataFrame:
        incomplete = (df.isna() | df.eq("")).any(axis=1)
        return df[~incomplete]


def collect(variants: Iterable[tuple[Source, dict[str, Any]]]) -> pd.DataFrame:
    frames = []
    for source, tags in variants:
        try:
            df = CsvExporter(source).to_frame()
        except requests.HTTPError as error:
            if error.response is not None and error.response.status_code == 404:
                log.warning("Skipping %s: not found", tags)
                continue
            raise
        frames.append(df.assign(**tags)[[*tags, *df.columns]])
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
