import pandas as pd
import streamlit as st


def show_error_table(df: pd.DataFrame):
    # Remove non-error activities
    df = df[~df.Error.isnull()]
    with st.expander("Errors list", expanded=True):
        st.write(f"Total errors: {len(df)}")
        # Take at most n elements
        df = df[: min(len(df), 30)]  # TODO: set to max 10
        _table_errors(df)


def _table_errors(df: pd.DataFrame):
    """Generate error table.

    Make table containing
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
    col3.write("**Activity**")
    col4.write("**Links**")
    for row in df.to_dict(orient="records"):
        # Col 1
        col1.write(row["Error"])
        # Col 2
        year = row["DTSTART"].year
        month = row["DTSTART"].month
        day = row["DTSTART"].day
        col2.write(f"{day}/{month}/{year}")
        # Col 3
        name_event = row["SUMMARY"]
        name_cal = row["Calendar"]
        # Take first n characters to not overflow
        col3.write(f"{name_event} ({name_cal})"[:20])
        # Col 4
        link_event = row["EVENT_LINK"]
        link_week = (
            f"https://calendar.google.com/calendar/u/0/r/week/{year}/{month}/{day}"
        )
        link_day = (
            f"https://calendar.google.com/calendar/u/0/r/day/{year}/{month}/{day}"
        )
        col4.write(f"[Event]({link_event}) [W]({link_week}) [D]({link_day})")
