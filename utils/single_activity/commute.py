import altair as alt
import pandas as pd
import streamlit as st

from utils.normalize import normalize_all_to_one_count
from utils.remove_last_month import remove_last_month
from utils.single_activity import (
    chart_calendar_vert,
    chart_decreasing_activity,
    group_by_period,
)


def commute(df: pd.DataFrame) -> None:
    df = df.copy()
    st.header("Commute")
    df = remove_last_month(df, "DTSTART")
    chart_walk_bus(df)
    chart_calendar_vert(df, "Commute")
    chart_decreasing_activity(df, "Commute")


def chart_walk_bus(df: pd.DataFrame) -> None:
    df = remove_last_month(df, "DTSTART")
    df = df.loc[df["SUMMARY"].isin(["Walk", "Bus", "Car", "Train"])]
    # Remove activities longer than 1 hour
    df = df.loc[df["Duration"] <= 1]
    df = group_by_period(df, "M")
    # Normalize all to one
    df = normalize_all_to_one_count(df, ["SUMMARY"])
    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
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
