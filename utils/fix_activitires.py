import base64
from urllib import parse
import streamlit as st
import pandas as pd


def fix_activities(df: pd.DataFrame):
    """Show list of all the activities that are broken.
    These activities may be broken due to:
    - A day does not have both
    https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/46
    """
    df = df.copy()
    df = _cal_link(df)
    _check_errors(df)
    df = df[~df.Error.isnull()]
    # Take at most n elements
    st.write(f"Total errors: {len(df)}")
    df = df[: min(len(df), 30)]
    _table_errors(df)


def _check_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Get errors from dataframe

    Args:
        df (pd.DataFrame): [description]

    Returns:
        pd.DataFrame: [description]
    """
    df["DTSTARTMIN"] = df["DTSTART"].dt.minute
    df["DTENDMIN"] = df["DTEND"].dt.minute
    df.loc[df["DTSTARTMIN"] == 15, "Error"] = "Starts at 15"
    df.loc[df["DTSTARTMIN"] == 45, "Error"] = "Starts at 45"
    df.loc[df["DTENDMIN"] == 15, "Error"] = "Ends at 15"
    df.loc[df["DTENDMIN"] == 45, "Error"] = "Ends at 45"
    df = df.drop(["DTSTARTMIN", "DTENDMIN"], axis=1)


def _cal_link(df: pd.DataFrame):
    """Compute calendar link described in:
    https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/58

    Columns taken into consideration:
    - UID: https://calendar.google.com/.../basic.ics
    - CAL_LINK: xxxxxxxxx@google.com
    """
    # From: 64xxxxxxxco@google.com
    # To:   64xxxxxxxco
    df["UID"] = df["UID"].str.split("@", expand=True)[0]
    # From: https://calendar.google.com/calendar/ical/t2xxxxxxxxxxxxxxxxxxxxx64%40group.calendar.google.com/private-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/basic.ics
    # To:   t2xxxxxxxxxxxxxxxxxxxxx64%40group.calendar.google.com
    df["CAL_LINK"] = df["CAL_LINK"].str.split("/", expand=True)[5]
    # %40 to @
    df["CAL_LINK"] = df["CAL_LINK"].apply(parse.unquote)
    # From: t2xxxxxxxxxxxxxxxxxxxxxx64@group.calendar.google.com
    # To:   t2xxxxxxxxxxxxxxxxxxxxxx64@g
    df["CAL_LINK"] = df["CAL_LINK"].str.split("@", expand=True)[0] + "@g"
    df["EVENT_LINK"] = df["UID"] + " " + df["CAL_LINK"]
    # String to bytes
    # TODO: try to remove strict
    df["EVENT_LINK"] = df["EVENT_LINK"].str.encode("utf-8", "strict")
    # Bytes to base64
    df["EVENT_LINK"] = df["EVENT_LINK"].apply(base64.b64encode)
    # Bytes to string
    df["EVENT_LINK"] = df["EVENT_LINK"].str.decode("utf-8")
    df["EVENT_LINK"] = (
        "https://calendar.google.com/calendar/u/0/r/eventedit/" + df["EVENT_LINK"]
    )
    return df


def _table_errors(df: pd.DataFrame):
    """Make table containing
    - Error type
    - Calendar: Personal care
    - Summary: e.g. Show
    - Event link

    Args:
        df (pd.DataFrame): Analyzed dataframe
    """
    # Kind of table
    col1, col2, col3, col4 = st.columns(4)
    col1.write("**Error type**")
    col2.write("**Calendar**")
    col3.write("**Summary**")
    col4.write("**Event link**")
    for row in df.to_dict(orient="records"):
        col1.write(row["Error"])
        col2.write(row["Calendar"])
        col3.write(row["SUMMARY"])
        link = row["EVENT_LINK"]
        col4.write(f"[Event link]({link})")
