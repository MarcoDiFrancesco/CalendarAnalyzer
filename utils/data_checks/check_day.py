import pandas as pd


def check_day(df: pd.DataFrame) -> None:
    """Check activity sequence in a day."""
    # Split day at 4:00am
    df_serie = df.resample(on="DTSTART", rule="24h", offset="4h 30m")
    for df_day in df_serie:
        # df_day is a
        _daily_checks(df, df_day[1])


def _daily_checks(df: pd.DataFrame, df_day: pd.DataFrame) -> None:
    """Wrapper of _check_consequent.

    Args:
        df (pd.DataFrame): input dataframe
        df_day (pd.DataFrame): tuple of 2 items, first the serie beginning date second the df
    """
    if len(df_day) >= 2:
        _check_consequent(df, df_day)


def _check_consequent(df: pd.DataFrame, df_day: pd.DataFrame) -> None:
    """Make gaps and serie checks.

    - Gaps: check if 2 consequent activities have a gap time in the middle
            Like Lunch ends at 13:00 and following Phone starts at 13:30
    - Serie: check if 2 consequent activities are the same.
             Like Phone at 10:00 and Phone at 10:30.
    """
    for i in range(len(df_day) - 1):
        # Activity before the gap
        act1 = df_day.iloc[i]
        # Activity after the gap
        act2 = df_day.iloc[i + 1]

        # Gaps
        if act1["DTEND"] != act2["DTSTART"]:
            gap_start = f"{act1['DTEND'].hour}:{act1['DTEND'].minute:02d}"
            gap_end = f"{act2['DTSTART'].hour}:{act2['DTSTART'].minute:02d}"
            df.loc[
                df["DTSTART"] == act2["DTSTART"], "Error"
            ] = f"Gap {gap_start} to {gap_end}"

        # Consequent
        # If Calendar is different than do mark as error
        # e.g. Walk (Commute) != Walk (Spare time)
        if act1["SUMMARY"] == act2["SUMMARY"] and act1["Calendar"] == act2["Calendar"]:
            act_start = f"{act2['DTSTART'].hour}:{act2['DTSTART'].minute:02d}"
            df.loc[
                df["DTSTART"] == act2["DTSTART"], "Error"
            ] = f"Same act ({act_start})"
