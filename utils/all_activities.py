import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.legend import legend
from utils.normalize import normalize_all_to_one
from utils.remove_last_month import remove_last_month


def chart_calendars(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalize_all_to_one(df)
    df = remove_last_month(df, "Period")
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(height=500)
        .encode(
            x=alt.X("Period", title="Month"),
            y=alt.Y(
                "sum(Duration)", title="Normalized duration", axis=alt.Axis(format="%")
            ),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
    )


def chart_calendars_longest(df: pd.DataFrame):
    st.subheader("Longest non-stop activities")
    df = df.copy()
    df = df.sort_values("Duration", ascending=False)
    df = df.drop_duplicates("SUMMARY")
    df = df.head(10)
    st.altair_chart(
        alt.Chart(df)
        .mark_bar(point=True)
        .properties(width=700, height=300)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y("SUMMARY", title="Activity", sort="-x"),
            color=alt.Color("Calendar", scale=legend(df)),
            tooltip=[
                alt.Tooltip("Duration", title="Duration (hours)"),
                alt.Tooltip("yearmonthdatehoursminutes(DTSTART)", title="Start date"),
                alt.Tooltip("yearmonthdatehoursminutes(DTEND)", title="End date"),
            ],
        )
    )


def time_quality(df: pd.DataFrame) -> None:
    st.subheader("Time quality")
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalize_all_to_one(df)
    df = remove_last_month(df, "Period")

    act_bad = ["Chores", "Commute", "Eat", "Entertainment", "Personal care"]
    df_bad = df.loc[df["Calendar"].isin(act_bad)]
    left = (
        alt.Chart(df_bad)
        .encode(
            y=alt.Y("Period:O", axis=None),
            x=alt.X("Duration", title="hourss", sort=alt.SortOrder("descending")),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
        .mark_bar()
        .properties(title="Bad", width=250)
    )
    middle = (
        alt.Chart(df)
        .encode(
            y=alt.Y("Period", axis=None),
            text=alt.Text("Period"),
        )
        .mark_text()
        .properties(width=50)
    )
    act_good = ["Personal development", "Spare time", "Sport", "Study", "Work"]
    df_good = df.loc[df["Calendar"].isin(act_good)]
    right = (
        alt.Chart(df_good)
        .encode(
            y=alt.Y("Period:O", axis=None),
            x=alt.X("Duration", title="hourss"),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
        .mark_bar()
        .properties(title="Good", width=250)
    )
    st.altair_chart(alt.concat(left, middle, right, spacing=5))
