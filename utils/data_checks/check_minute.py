import pandas as pd


def check_minute(df: pd.DataFrame):
    """Get errors from dataframe"""
    df["DTSTARTMIN"] = df["DTSTART"].dt.minute
    df["DTENDMIN"] = df["DTEND"].dt.minute
    df.loc[df["DTSTARTMIN"] == 15, "Error"] = "Starts at 15"
    df.loc[df["DTSTARTMIN"] == 45, "Error"] = "Starts at 45"
    df.loc[df["DTENDMIN"] == 15, "Error"] = "Ends at 15"
    df.loc[df["DTENDMIN"] == 45, "Error"] = "Ends at 45"
    df.drop(["DTSTARTMIN", "DTENDMIN"], axis=1, inplace=True)
