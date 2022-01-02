from utils.group_by_period import group_by_period
from utils.normalize import normalized_duration
from utils.remove_last_month import remove_last_month
import streamlit as st
import altair as alt
import pandas as pd


def chart_calendar(df: pd.DataFrame, calendar: str):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = normalized_duration(df)
    df = remove_last_month(df, "Period")
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


def select_activity(df: pd.DataFrame) -> str:
    cal_list = df.Calendar.unique()
    cal_list = sorted(cal_list, reverse=True)
    # Added a separate section for it
    cal_list.remove("Entertainment")
    # cal_list.remove("Sport")
    return st.radio("List of all calendars", cal_list)
