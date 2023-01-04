import time

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
    month_count = len(df.Period.unique())
    st.altair_chart(
        alt.Chart(df, width={"step": 0.45 * month_count})
        .mark_bar()
        .properties(height=500, width=780)
        .encode(
            x=alt.X("Period", title="Month"),
            y=alt.Y(
                "sum(Duration)",
                title="Normalized duration",
                axis=alt.Axis(format="%"),
                scale=alt.Scale(domain=[0, 1]),
            ),
            color=alt.Color(
                "Calendar",
                scale=legend(df, "Calendar"),
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
            color=alt.Color("Calendar", scale=legend(df, "Calendar")),
            tooltip=[
                alt.Tooltip("Duration", title="Duration (hours)"),
                alt.Tooltip("yearmonthdatehoursminutes(DTSTART)", title="Start date"),
                alt.Tooltip("yearmonthdatehoursminutes(DTEND)", title="End date"),
            ],
        )
    )


def time_quality(df: pd.DataFrame) -> None:
    st.subheader("Productivity index")
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalize_all_to_one(df)
    df = remove_last_month(df, "Period")

    act_bad = ["Chores", "Commute", "Eat", "Entertainment", "Personal care"]
    act_good = [e for e in df["Calendar"].unique() if e not in act_bad]
    st.markdown(
        f"""
        Bad: {act_bad}

        Good: {act_good}
        """
    )

    df_bad = df.loc[df["Calendar"].isin(act_bad)]
    left = (
        alt.Chart(df_bad)
        .encode(
            y=alt.Y("Period:O", axis=None),
            x=alt.X("Duration", title="hourss", sort=alt.SortOrder("descending")),
            color=alt.value("#eb4034"),  # Red
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
        .mark_bar()
        .properties(title="Bad", width=250, height=500)
    )
    middle = (
        alt.Chart(df)
        .encode(
            y=alt.Y("Period", axis=None),
            text=alt.Text("Period"),
        )
        .mark_text()
        .properties(width=50, height=500)
    )
    act_good = ["Personal development", "Spare time", "Sport", "Study", "Work"]
    df_good = df.loc[df["Calendar"].isin(act_good)]
    right = (
        alt.Chart(df_good)
        .encode(
            y=alt.Y("Period:O", axis=None),
            x=alt.X("Duration", title="hourss"),
            color=alt.value("#3dbf4a"),  # Green
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
        .mark_bar()
        .properties(title="Good", width=250, height=500)
    )
    st.altair_chart(alt.concat(left, middle, right, spacing=5))


def night_sleep_distribution(df: pd.DataFrame) -> None:
    st.markdown(
        """
        ### Night sleep length distribution
        """
    )
    df = df.copy()
    df = _compute_sleep(df)
    chart = (
        alt.Chart(df)
        .mark_bar(opacity=0.7, size=460 / len(df))
        .properties(width=670, height=350)
        .encode(
            x=alt.X("diff", title="Number of hours slept"),
            y=alt.Y("count", title="Day count"),
            tooltip=[
                alt.Tooltip("diff", title="Hours slept"),
                alt.Tooltip("count", title="Number of times"),
            ],
        )
        .configure_mark(color="#555657")
    )
    st.altair_chart(chart)


def _compute_sleep(df: pd.DataFrame) -> pd.DataFrame:
    """Computes gap between activities, equivalent to sleep during the night.

    Sleep during the day is ignored for the scope of this plot.

    Returns:
                  diff  count  diff_hours
    0  0 days 05:00:00      6         5.0
    1  0 days 05:30:00      5         5.5
    2  0 days 06:00:00     10         6.0
    """
    sleep_ls = []
    arr = df.to_numpy()
    # Performance of this for loop: for 15.000 rows, 3 years of data, takes 0.074 sec
    for i in range(len(df) - 1):
        # Activity before the gap
        _, act1_start, act1_end, _, _, _, _, _ = arr[i]
        # Activity after the gap
        _, act2_start, act2_end, _, _, _, _, _ = arr[i + 1]
        # Gaps
        if act1_end != act2_start:
            sleep_ls.append((act1_end, act2_start))

    df_sleep = pd.DataFrame(sleep_ls, columns=["start", "end"])
    df_sleep["diff"] = df_sleep["end"] - df_sleep["start"]
    df_sleep = df_sleep.groupby("diff").count()
    df_sleep = (
        df_sleep.drop("end", axis=1).rename({"start": "count"}, axis=1).reset_index()
    )
    df_sleep["diff"] = df_sleep["diff"].dt.seconds / 3600
    return df_sleep
