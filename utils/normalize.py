import pandas as pd


def normalize_max_to_one(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize biggest columns to one"""
    return df


def normalize_all_to_one(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize all columns to 1"""
    df_sum = df.groupby(["Period"]).sum().reset_index()
    df_sum = df_sum.rename(columns={"Duration": "Duration_Month"})
    df_new = pd.merge(df, df_sum, on="Period")
    df_new["Duration_Normalized"] = df_new["Duration"] / df_new["Duration_Month"]
    df["Duration"] = df_new["Duration_Normalized"]
    return df


def normalized_duration(df):
    """
    Normalize activity duration by number of days in the month
    e.g. 10h activity in February -> 10h * 30 / 28 = 10.71h
    """
    df_date = pd.DataFrame(df["Period"])
    df_date["Period"] = pd.to_datetime(df_date["Period"])
    df_date["DaysInMonth"] = df_date["Period"].dt.daysinmonth
    df["Duration"] = df["Duration"] * 30 / df_date["DaysInMonth"]
    return df
