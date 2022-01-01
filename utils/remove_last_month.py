import datetime
import pandas as pd


def remove_last_month(df: pd.DataFrame, column_name: str = "Period") -> pd.DataFrame:
    """Remove last month of data from dataframe
    Set here and not in Calendar class so it's possible to filter data
    only in charts and not in table."""
    month = datetime.datetime.today().strftime("%Y-%m")
    return df[df[column_name] < month]
