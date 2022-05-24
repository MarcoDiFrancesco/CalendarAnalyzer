import pandas as pd


def normalize_to_average(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize with aveage being to 1.

    Calculated as: sum_of_hours / months_number
    """
    df["Duration"] /= df["Duration"].sum() / len(df["Period"].unique())
    return df


def normalize_all_to_one(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize all columns to sum by 1."""
    df_sum = df.groupby(["Period"]).sum().reset_index()
    df_sum = df_sum.rename(columns={"Duration": "Duration_Month"})
    df_new = pd.merge(df, df_sum, on="Period")
    df_new["Duration_Normalized"] = df_new["Duration"] / df_new["Duration_Month"]
    df["Duration"] = df_new["Duration_Normalized"]
    return df


def normalize_all_to_one_count(df: pd.DataFrame, group_by: list) -> pd.DataFrame:
    """Normalize all columns to 1 by Period.

    Args:
        df (pd.DataFrame): Input dataframe
        group_by (list): List of what to group by other than Period, e.g. ["SUMMARY"]

    Returns:
        pd.DataFrame: Output dataframe
    """
    # Dataframe for counting months occurrences
    df_month = df[["Period", "Duration"]]
    df_month = df_month.groupby(["Period"]).count().reset_index()
    df = df[["Period", *group_by, "Duration"]]
    df = df.groupby(["Period", *group_by]).count().reset_index()
    # Dataframe with both Duration_month (12) and Duration_group (7)
    df = pd.merge(df_month, df, on="Period", suffixes=("_month", "_group"))
    # Division throws warning if not float
    df["Duration_group"].astype("float")
    df["Duration_month"].astype("float")
    # Duration becomes 0.58
    df["Duration"] = df["Duration_group"] / df["Duration_month"]
    return df


def normalized_duration(df):
    """Normalize activity duration by number of days in the month.

    e.g. 10h activity in February -> 10h * 30 / 28 = 10.71h
    """
    df_date = pd.DataFrame(df["Period"])
    df_date["Period"] = pd.to_datetime(df_date["Period"])
    df_date["DaysInMonth"] = df_date["Period"].dt.daysinmonth
    df["Duration"] = df["Duration"] * 30 / df_date["DaysInMonth"]
    return df
