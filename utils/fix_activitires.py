import base64
from urllib import parse

import pandas as pd
import streamlit as st


def fix_activities(df: pd.DataFrame):
    """Show list of all the activities that are broken.
    These activities may be broken due to:
    - A day does not have both
    https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/46
    """
    df = df.copy()
    df = _cal_link(df)
    _check_minute(df)
    _check_meal(df)
    df = df[~df.Error.isnull()]
    with st.expander("Errors list", expanded=True):
        st.write(f"Total errors: {len(df)}")
        # Take at most n elements
        df = df[: min(len(df), 10)]
        _table_errors(df)


def _check_minute(df: pd.DataFrame):
    """Get errors from dataframe"""
    df["DTSTARTMIN"] = df["DTSTART"].dt.minute
    df["DTENDMIN"] = df["DTEND"].dt.minute
    df.loc[df["DTSTARTMIN"] == 15, "Error"] = "Starts at 15"
    df.loc[df["DTSTARTMIN"] == 45, "Error"] = "Starts at 45"
    df.loc[df["DTENDMIN"] == 15, "Error"] = "Ends at 15"
    df.loc[df["DTENDMIN"] == 45, "Error"] = "Ends at 45"
    df.drop(["DTSTARTMIN", "DTENDMIN"], axis=1, inplace=True)


def _check_meal(df: pd.DataFrame):
    df = df.head(50)
    # TODO: impelement other daily checks using this function
    # df.groupby("DAY").apply(_check_meal_day)


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
    col2.write("**Day**")
    col3.write("**Name**")
    col4.write("**Event link**")
    for row in df.to_dict(orient="records"):
        col1.write(row["Error"])
        year = row["DTSTART"].year
        month = row["DTSTART"].month
        day = row["DTSTART"].day
        col2.write(f"{day}/{month}/{year}")
        name_event = row["SUMMARY"]
        name_cal = row["Calendar"]
        # Take first n characters to not overflow
        col3.write(f"{name_event} ({name_cal})"[:20])
        link_event = row["EVENT_LINK"]
        link_week = (
            f"https://calendar.google.com/calendar/u/0/r/week/{year}/{month}/{day}"
        )
        col4.write(f"[Event]({link_event}) [Week]({link_week})")
