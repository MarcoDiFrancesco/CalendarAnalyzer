import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.legend import legend
from utils.normalize import normalize_all_to_one
from utils.remove_last_month import remove_last_month
from utils.single_activity.eat import _filter_first_daily_activity


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


def average_activity_time(df: pd.DataFrame) -> None:
    st.subheader("Average activity time")
    df = df.copy()
    # Filter for debugging readibility
    df = df[["Calendar", "SUMMARY", "DTSTART"]]

    # Consider only first activity of the day
    df = _filter_first_daily_activity(df, "SUMMARY")

    # Group by month and remvoe the last one
    df = group_by_period(df, "M")
    df = remove_last_month(df, "Period")

    # Take time from DTSTART
    df["Time"] = df["DTSTART"].dt.time
    df["Time"] = pd.to_timedelta(df["Time"].astype(str))

    # Not selecting raises warning
    df = df[["Time", "Period", "SUMMARY"]].groupby(["Period", "SUMMARY"]).mean()
    df = df.reset_index()

    # TimeDelta to TimeDate
    df = df.assign(TimeDate=0)
    df["TimeDate"] = pd.to_datetime(df["TimeDate"])
    df["TimeDate"] += df["Time"]
    # Drop for readibility
    df = df.drop("Time", axis=1)

    # Select few activities
    df = df[df["SUMMARY"].isin(["Breakfast", "Lunch", "Dinner"])]

    st.altair_chart(
        alt.Chart(df)
        .mark_line()
        .properties(width=700, height=400)
        .encode(
            alt.X("Period"),
            alt.Y("hoursminutes(TimeDate):T", title="Time"),
            color=alt.Color("SUMMARY"),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("hoursminutes(TimeDate):T", title="Average time"),
                alt.Tooltip("Period"),
            ],
        )
    )
