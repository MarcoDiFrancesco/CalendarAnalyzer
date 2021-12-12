import os

import pandas as pd
import streamlit as st
from streamlit.legacy_caching import clear_cache
from urllib import parse
import base64


def get_password(df: pd.DataFrame) -> pd.DataFrame:
    """Return true if password is correct"""
    with st.expander("Admin"):
        password = st.text_input("Enter a password", type="password")
        # TODO: check if this flag works
        if os.environ.get("DEBUG"):
            caching_button()
            fix_activities(df)
            return df
        if password == os.environ.get("PSW"):
            caching_button()
            fix_activities(df)
            return df
    df = df[df.Calendar != "Work"]
    return df


def caching_button():
    btn = st.button("Clear cache")
    if btn:
        clear_cache()


def fix_activities(df: pd.DataFrame):
    """Show list of all the activities that are broken.
    These activities may be broken due to:
    - A day does not have both
    https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/46
    """
    df = df.copy()
    df = _cal_link(df)
    df = _check_time(df)
    df = df[: min(len(df), 100)]
    df = df.filter(["Calendar", "SUMMARY", "DTSTART", "EVENT_LINK"])
    st.table(df)


def _check_time(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["DTSTART"].dt.minute == 15) | (df["DTSTART"].dt.minute == 45)]


def _cal_link(df: pd.DataFrame):
    """Compute calendar link described in:
    https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/58

    Columns taken into consideration:
    - UID: https://calendar.google.com/.../basic.ics
    - CAL_LINK: xxxxxxxxx@google.com
    """
    # df = df.head(2).copy()
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
