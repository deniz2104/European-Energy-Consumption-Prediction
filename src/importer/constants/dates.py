import pandas as pd
from typing import Final

TODAY = pd.Timestamp.today().normalize()
END_DATE: Final[str] = (TODAY - pd.Timedelta(days=5)).date().isoformat()
START_DATE: Final[str] = (pd.Timestamp(END_DATE) - pd.DateOffset(years=3)).date().isoformat()
YEARS: Final[list[int]] = list(range(pd.Timestamp(START_DATE).year, pd.Timestamp(END_DATE).year + 1))
