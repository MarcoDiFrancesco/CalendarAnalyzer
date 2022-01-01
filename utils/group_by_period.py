import warnings
import pandas as pd


def group_by_period(df: pd.DataFrame, period: str) -> pd.DataFrame:
    """Group by period and make sum of the hours and normalize duration to it's size"""
    # Hide warning: Converting to PeriodArray/Index representation
    # will drop timezone information.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df["Period"] = df["DTSTART"].dt.to_period(period).astype("str")
    return df
