import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.normalize import normalized_duration
from utils.remove_last_month import remove_last_month


def filter_df_chart(df: pd.DataFrame, calendar: str):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = df.loc[df["Calendar"] == calendar]
    return df


def chart_calendar_vert(df: pd.DataFrame, calendar: str):
    # TODO: remove this function once all categories are splitted
    df = filter_df_chart(df, calendar)
    df = normalized_duration(df)
    # Horizotal chart does not require last month to be removed
    df = remove_last_month(df, "Period")

    st.altair_chart(
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
        .configure_legend(labelLimit=120),
        # use_container_width=True,
    )


def chart_decreasing_activity(df: pd.DataFrame, calendar: str):
    # TODO: remove this function once all categories are splitted
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
    cal_list.remove("Sport")
    cal_list.remove("Study")
    return st.radio("List of all calendars", cal_list)
