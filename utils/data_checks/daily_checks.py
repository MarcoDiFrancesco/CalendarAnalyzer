import pandas as pd


def daily_checks(df: pd.DataFrame):
    """Check activity sequence in a day"""
    # Split day at 5am
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
    for i in range(len(df_day) - 1):
        if df_day.iloc[i]["DTEND"] != df_day.iloc[i + 1]["DTSTART"]:
            # Activity before the gap
            act1 = df_day.iloc[i]
            # Activity after the gap
            act2 = df_day.iloc[i + 1]
            gap_start = f"{act1['DTEND'].hour}:{act1['DTEND'].minute:02d}"
            gap_end = f"{act2['DTSTART'].hour}:{act2['DTSTART'].minute:02d}"
            df.loc[
                df["DTSTART"] == act2["DTSTART"], "Error"
            ] = f"Gap {gap_start} to {gap_end}"
            # print(gap_start, gap_end)
            # print(df_day)


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
