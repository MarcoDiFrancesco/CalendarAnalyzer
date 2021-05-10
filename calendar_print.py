from altair.vegalite.v4.schema.core import Axis
import pandas as pd
import streamlit as st

from utils import get_google_calendars
import warnings


def edit_datetime(calendars):
    for name, events in calendars.items():
        # Transforms dates in date format
        events["DTSTART"] = pd.to_datetime(events["DTSTART"])
        events["DTEND"] = pd.to_datetime(events["DTEND"])

        # Calculates duration from start to end like:
        #     Groceries	0 days 01:00:00
        # Transform to minutes:
        #     Groceries	1
        events["Duration"] = events["DTEND"] - events["DTSTART"]
        events["Duration"] = events["Duration"].dt.total_seconds() / 60 / 60

        # Add index
        # From:
        #     1	Groceries	0 days 01:00:00
        #     2	Shopping	0 days 01:00:00
        #     3	Groceries	0 days 01:00:00
        # With index:
        #     Groceries	0 days 01:00:00
        #     Shopping	0 days 01:00:00
        #     Groceries	0 days 01:00:00
        # events = events.set_index("SUMMARY")

        # Sort by duration descending
        events = events.sort_values(by=["Duration", "SUMMARY"], ascending=False)

        # Remove daily or mulitple days activities
        events = events[events.Duration != 0]
        calendars[name] = events
    return calendars


def show_by_activity(calendars):
    """
    Show list of activities with duration:
    Algoritmi	45
    Reti	    44.5000
    Ingegneria 	39
    """
    activities = ["Select value", *calendars]
    activity = st.selectbox("List of all the activities", activities)
    if activity != "Select value":
        st.table(calendars[activity])


def get_by_activity(calendars):
    # Sum:
    #     Groceries	0 days 02:00:00
    #     Shopping	0 days 01:00:00
    for name, events in calendars.items():
        events = events.sum()
    return calendars


def get_by_month(calendars):
    # 2021-03 FBK         3.00
    #         Update      1.00
    # 2021-04 FBK         2.0
    #         Update      4.00
    for name, df in calendars.items():
        # Hide warning: Converting to PeriodArray/Index representation will drop timezone information.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df["Month"] = df["DTSTART"].dt.to_period("M").astype("str")
        df.set_index(["Month", "SUMMARY"], inplace=True)
        df = df.groupby(["Month", "SUMMARY"])
        df = df.sum()
        calendars[name] = df
    return calendars


if __name__ == "__main__":
    calendars = get_google_calendars()
    calendars = calendars.copy()
    calendars = edit_datetime(calendars)

    st.title("Calendar Analyzer")
    data_by_activity = get_by_activity(calendars)
    data_by_month = get_by_month(calendars)
    show_by_activity(data_by_month)

    # for name, calendar in data_by_month.items():
    #     st.bar_chart(calendar)
