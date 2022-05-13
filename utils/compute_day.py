from datetime import timedelta

import pandas as pd


def compute_day(df: pd.DataFrame):
    """Add date column (DAY) with format YY-MM-DD."""
    df_start = df["DTSTART"]
    df_start = df_start - timedelta(hours=5)
    df["DAY"] = df_start.dt.strftime("%Y-%m-%d")
