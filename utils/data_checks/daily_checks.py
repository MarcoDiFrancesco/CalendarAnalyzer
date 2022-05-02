import pandas as pd


def daily_checks(df: pd.DataFrame):
    """Check activity sequence in a day"""
    df = df.head(100)
    df_serie = df.resample(on="DTSTART", rule="24h", offset="5h")
    for df_day in df_serie:
        # daily_activities is a tuple of 2 items, first the serie beginning date second the df
        _daily_checks(df, df_day[1])


def _daily_checks(df: pd.DataFrame, df_day: pd.DataFrame):
    if len(df_day) >= 2:
        _check_gaps(df, df_day)
        # _check_serie(df, df_day)
        # _check_meal_day(df)


def _check_gaps(df: pd.DataFrame, df_day: pd.DataFrame):
    """Check if 2 consequent activities have a gap time in the middle.
    Like Lunch ends at 13:00 and following Phone starts at 13:30.
    """
    # print(type(df_day))
    for i in range(len(df_day) - 1):
        if df_day.iloc[i]["DTEND"] != df_day.iloc[i + 1]["DTSTART"]:
            print("-----", df_day.iloc[i]["DTEND"])
            print("=====", df_day.iloc[i + 1]["DTSTART"])
            print(df_day)
            print("TODO: shift the time (2 hours out), understand the freaking problem")
            df.loc[df["DTSTART"] == df_day.iloc[i]["DTSTART"], "Error"] = "Gap"


def _check_serie(df: pd.DataFrame):
    """Check if 2 consequent activities are the same.
    Like Phone at 10:00 and Phone at 10:30.
    """
    # print("_check_gaps", df)
    raise NotImplementedError


def _check_meal_day(df: pd.DataFrame):
    """Check for meal in this order
    - Breakfast
    - Lunch
    - Dinner

    Args:
        df (pd.DataFrame): Datafram with all the activities in a day
    """
    df = df[df["SUMMARY"].isin(["Breakfast", "Lunch", "Dinner"])]
    raise NotImplementedError
