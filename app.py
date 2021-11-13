import datetime
import warnings

import altair as alt
import pandas as pd
import streamlit as st
from streamlit.commands.page_config import set_page_config

from utils import clean_df, password
from utils.download_cals import download_cals
from utils.table_sum import table_sum


def select_activity(df: pd.DataFrame) -> str:
    cal_list = df.Calendar.unique()
    return st.radio("List of all calendars", cal_list)


def chart_all(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = _get_normalized_duration(df)
    df = normalize_to_one(df)
    df = remove_last_month(df)
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=400)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Sum of hours"),
            color=alt.Color(
                "Calendar",
                scale=alt.Scale(
                    domain=[
                        "Chores",
                        "Commute",
                        "Eat",
                        "Entertainment",
                        "Personal care",
                        "Personal development",
                        "Spare time",
                        "Sport",
                        "Study",
                        "Work",
                    ],
                    range=[
                        "#7986CB",
                        "#9E69AF",
                        "#039BE5",
                        "#F4511E",
                        "#E67C73",
                        "#F6BF26",
                        "#B39DDB",
                        "#8E24AA",
                        "#33B679",
                        "#F09300",
                    ],
                ),
                legend=alt.Legend(title="Color Legend"),
            ),
        )
    )


def chart_single(df: pd.DataFrame, calendar: str):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = _get_normalized_duration(df)
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
                legend=alt.Legend(title="Color Legend"),
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
        .properties(width=700, height=500)
        .encode(
            alt.X("SUMMARY", sort="-y"),
            alt.Y("Duration", title="Hours"),
            color=alt.Color("SUMMARY", legend=None),
        )
    )


def _get_normalized_duration(df):
    """
    Normalize activity duration by number of days in the month
    e.g. 10h activity in February -> 10h * 30 / 28 = 10.71h
    """
    df_date = pd.DataFrame(df["Period"])
    df_date["Period"] = pd.to_datetime(df_date["Period"])
    df_date["DaysInMonth"] = df_date["Period"].dt.daysinmonth
    df["Duration"] = df["Duration"] * 30 / df_date["DaysInMonth"]
    return df


def group_by_period(df: pd.DataFrame, period: str) -> pd.DataFrame:
    """Group by period and make sum of the hours and normalize duration to it's size"""
    # Hide warning: Converting to PeriodArray/Index representation
    # will drop timezone information.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df["Period"] = df["DTSTART"].dt.to_period(period).astype("str")
    return df


def normalize_to_one(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize data to 1"""
    df_sum = df.groupby(["Period"]).sum().reset_index()
    df_sum = df_sum.rename(columns={"Duration": "Duration_Month"})
    df_new = pd.merge(df, df_sum, on="Period")
    df_new["Duration_Normalized"] = df_new["Duration"] / df_new["Duration_Month"]
    df["Duration"] = df_new["Duration_Normalized"]
    return df


def remove_last_month(df: pd.DataFrame) -> pd.DataFrame:
    """Remove last month of data from dataframe
    Set here and not in Calendar class so it's possible to filter data
    only in charts and not in table."""
    month = datetime.datetime.today().strftime("%Y-%m")
    return df[df["Period"] < month]


set_page_config(page_title="Calendar Analyzer", page_icon="⌛")
st.title("Calendar Analyzer")
st.caption(
    "[https://github.com/MarcoDiFrancesco/CalendarAnalyzer](https://github.com/MarcoDiFrancesco/CalendarAnalyzer)"
)

df = download_cals().copy()
df = clean_df.clean_df(df)

df = password.get_password(df)

# All activities
st.markdown("---")
st.header("All activities")
# # TODO: remove work from dataframe
chart_all(df)
table_sum(df)

# Selected activity
st.markdown("---")
st.header("Single activity")
calendar = select_activity(df)
chart_single(df, calendar)
# df_by_activity = calendar.by_activity(sel_cal)
chart_decreasing_activity(df, calendar)
table_sum(df, calendar)
