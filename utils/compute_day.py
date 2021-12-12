import pandas as pd
from datetime import timedelta


def compute_day(df: pd.DataFrame):
    df_start = df["DTSTART"]
    df_start = df_start - timedelta(hours=5)
    df["DAY"] = df_start.dt.strftime("%Y-%m-%d")
