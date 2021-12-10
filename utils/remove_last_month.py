import datetime
import pandas as pd


def remove_last_month(df: pd.DataFrame) -> pd.DataFrame:
    """Remove last month of data from dataframe
    Set here and not in Calendar class so it's possible to filter data
    only in charts and not in table."""
    month = datetime.datetime.today().strftime("%Y-%m")
    return df[df["Period"] < month]
