import pandas as pd


def check_minute(df: pd.DataFrame):
    _check_quarter(df)
    _check_meal_day(df)


def _check_quarter(df: pd.DataFrame) -> None:
    """Get errors from dataframe"""
    df["DTSTARTMIN"] = df["DTSTART"].dt.minute
    df["DTENDMIN"] = df["DTEND"].dt.minute
    df.loc[df["DTSTARTMIN"] == 15, "Error"] = "Starts at 15"
    df.loc[df["DTSTARTMIN"] == 45, "Error"] = "Starts at 45"
    df.loc[df["DTENDMIN"] == 15, "Error"] = "Ends at 15"
    df.loc[df["DTENDMIN"] == 45, "Error"] = "Ends at 45"
    df.drop(["DTSTARTMIN", "DTENDMIN"], axis=1, inplace=True)


def _check_meal_day(df: pd.DataFrame) -> None:
    """Check for meals time start, snacks are included in one of those meals

    e.g. Breakfast can start at 11:30 but cannot start at 12:00
    """
    meals = {
        "Breakfast": {"start": "00:00", "end": "11:59"},
        "Lunch": {"start": "12:00", "end": "15:59"},
        "Dinner": {"start": "16:00", "end": "23:59"},
    }
    for meal, times in meals.items():
        df_meal = df[df["SUMMARY"].isin(meals.keys())]
        index = pd.DatetimeIndex(df_meal["DTSTART"])
        idx_b = index.indexer_between_time(times["start"], times["end"])
        df_b = df_meal.iloc[idx_b]
        df_b = df_b.loc[df_b["SUMMARY"] != meal]
        df.loc[
            df["DTSTART"].isin(df_b["DTSTART"]), "Error"
        ] = f"Is {meal} (<{times['end']})"
        # print(df_b)
