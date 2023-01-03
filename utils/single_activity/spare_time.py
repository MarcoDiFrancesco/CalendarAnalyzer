import warnings

import altair as alt
import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def spare_time(df: pd.DataFrame) -> None:
    df = df.copy()
    df = df[df["Calendar"] == "Spare time"]
    st.header("Spare time")
    df = remove_last_month(df, "DTSTART")
    _chart_calendar_vert(df)
    _chart_decreasing_activity(df)
    _susanna_call(df)


def _chart_calendar_vert(df: pd.DataFrame):
    df = filter_df_chart(df, "Spare time")
    # Horizontal chart does not require last month to be removed
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


def _chart_decreasing_activity(df: pd.DataFrame):
    df = df.copy()
    df = df.loc[df["Calendar"] == "Spare time"]
    df = df.groupby(["SUMMARY"]).sum().reset_index()
    st.write(
        alt.Chart(df)
        .mark_bar(point=True, opacity=0.9)
        .properties(width=550, height=300)
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


def _susanna_call(df: pd.DataFrame):
    st.markdown("### Call Susanna Frequency")
    df = df.copy()
    df = df.loc[df["SUMMARY"] == "Call Susanna"]
    df = df[["SUMMARY", "DTSTART"]]
    df = df.set_index("SUMMARY")
    df["TIMEDELTA"] = df.diff()["DTSTART"].dt.days
    # Ignoring FutureWarning: Dropping of nuisance columns in rolling operations is deprecated; in a future version this will raise TypeError.
    # I'm too lazy to fix it
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        # Rolling mean
        df["DAYSMEAN"] = df.rolling(6).mean()["TIMEDELTA"]
    df = df.reset_index()

    dots = (
        alt.Chart(df)
        .mark_line()
        .mark_circle(opacity=0.5)
        .properties(width=650, height=300)
        .encode(
            alt.X("DTSTART", title="Date"),
            alt.Y("DAYSMEAN", title="Days mean"),
        )
    )
    full = dots + dots.transform_loess(
        "DTSTART",
        "DAYSMEAN",
    ).mark_line(size=3)

    st.altair_chart(full)
