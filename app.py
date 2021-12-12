import warnings

import altair as alt
import pandas as pd
import streamlit as st
from streamlit.commands.page_config import set_page_config

from utils import clean_df, admin
from utils.download_cals import download_cals
from utils.table_sum import table_sum
from utils.remove_last_month import remove_last_month
from utils.normalize import normalize_to_one, normalized_duration
from utils.legend import legend


def select_activity(df: pd.DataFrame) -> str:
    cal_list = df.Calendar.unique()
    return st.radio("List of all calendars", cal_list)


def chart_calendars(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalized_duration(df)
    df = normalize_to_one(df)
    df = remove_last_month(df)
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=500)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Normalized duration"),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
        )
    )


def chart_calendar(df: pd.DataFrame, calendar: str):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = normalized_duration(df)
    df = remove_last_month(df)
    df = df.loc[df["Calendar"] == calendar]
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=500)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours"),
            color=alt.Color(
                "SUMMARY",
                legend=alt.Legend(title="Activity"),
            ),
        )
        .configure_legend(labelLimit=120)
    )


def chart_decreasing_activity(df: pd.DataFrame, calendar: str):
    df = df.copy()
    df = df.loc[df["Calendar"] == calendar]
    df = df.groupby(["SUMMARY"]).sum().reset_index()
    st.write(
        alt.Chart(df)
        .mark_bar(point=True)
        .properties(width=550, height=500)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y("SUMMARY", title="Activity", sort="-x"),
            color=alt.Color("SUMMARY", legend=None),
        )
    )


def chart_calendars_longest(df: pd.DataFrame):
    st.subheader("Longest non-stop activities")
    df = df.copy()
    # df = df.groupby(["Calendar", "SUMMARY"]).sum().reset_index()
    df = df.sort_values("Duration", ascending=False)
    df = df.drop_duplicates("SUMMARY")
    df = df.head(10)
    st.write(
        alt.Chart(df)
        .mark_bar(point=True)
        .properties(width=700, height=300)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y("SUMMARY", title="Activity", sort="-x"),
            color=alt.Color("Calendar", scale=legend(df)),
        )
    )


def group_by_period(df: pd.DataFrame, period: str) -> pd.DataFrame:
    """Group by period and make sum of the hours and normalize duration to it's size"""
    # Hide warning: Converting to PeriodArray/Index representation
    # will drop timezone information.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df["Period"] = df["DTSTART"].dt.to_period(period).astype("str")
    return df


set_page_config(page_title="Calendar Analyzer", page_icon="⌛")
st.title("Calendar Analyzer")
st.caption(
    "[https://github.com/MarcoDiFrancesco/CalendarAnalyzer](https://github.com/MarcoDiFrancesco/CalendarAnalyzer)"
)

df = download_cals().copy()
df = clean_df.clean_df(df)

df = admin.get_password(df)

# All activities
st.markdown("---")
st.header("All activities")
chart_calendars(df)
chart_calendars_longest(df)
table_sum(df)

# Selected activity
st.markdown("---")
st.header("Single activity")
st.text("Unique activities divided by calendar")
calendar = select_activity(df)
chart_calendar(df, calendar)
chart_decreasing_activity(df, calendar)
table_sum(df, calendar)
