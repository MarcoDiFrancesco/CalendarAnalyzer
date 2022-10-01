import altair as alt
import pandas as pd
import streamlit as st

from utils.normalize import normalize_all_to_one_count
from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart, group_by_period


def commute(df: pd.DataFrame) -> None:
    df = df.copy()
    st.header("Commute")
    df = remove_last_month(df, "DTSTART")
    chart_walk_bus(df)
    # TODO: Remove argument Calendar
    _chart_calendar_vert(df, "Commute")
    _chart_decreasing_activity(df, "Commute")


def chart_walk_bus(df: pd.DataFrame) -> None:
    df = remove_last_month(df, "DTSTART")
    df = df.loc[df["SUMMARY"].isin(["Walk", "Bus", "Car", "Train"])]
    # Remove activities longer than 1 hour
    df = df.loc[df["Duration"] <= 1]
    df = group_by_period(df, "Q")
    # Normalize all to one
    df = normalize_all_to_one_count(df, ["SUMMARY"])
    st.altair_chart(
        alt.Chart(df)
        .mark_area(opacity=0.9)
        .properties(width=700, height=350)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours", axis=alt.Axis(format="%")),
            color=alt.Color("SUMMARY", legend=alt.Legend(title="Activity")),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("Duration_group", title="Frequency activity"),
                alt.Tooltip("Duration_month", title="Frequency month"),
            ],
        )
        .configure_legend(labelLimit=120),
    )


def _chart_calendar_vert(df: pd.DataFrame, calendar: str):
    df = filter_df_chart(df, calendar)
    # Horizotal chart does not require last month to be removed
    df = remove_last_month(df, "Period")

    st.altair_chart(
        alt.Chart(df)
        .mark_bar(opacity=0.9)
        .properties(width=700, height=500)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours"),
            color=alt.Color("SUMMARY", legend=alt.Legend(title="Activity")),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("sum(Duration)", title="Total duration (hours)"),
            ],
        )
        .configure_legend(labelLimit=120),
    )


def _chart_decreasing_activity(df: pd.DataFrame, calendar: str):
    df = df.copy()
    df = df.loc[df["Calendar"] == calendar]
    df = df.groupby(["SUMMARY"]).sum().reset_index()
    st.write(
        alt.Chart(df)
        .mark_bar(point=True, opacity=0.9)
        .properties(width=550, height=350)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y("SUMMARY", title="Activity", sort="-x"),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("Duration", title="Total duration (hours)", format=".0f"),
            ],
            color=alt.Color("SUMMARY", legend=None),
        )
    )
