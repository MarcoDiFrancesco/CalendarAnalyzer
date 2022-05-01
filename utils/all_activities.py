import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.legend import legend
from utils.normalize import normalize_all_to_one, normalized_duration
from utils.remove_last_month import remove_last_month


def chart_calendars(df: pd.DataFrame):
    # TODO: move it to calendars
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalized_duration(df)
    df = normalize_all_to_one(df)
    df = remove_last_month(df, "Period")
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(height=500)
        .encode(
            x=alt.X("Period", title="Month"),
            y=alt.Y("sum(Duration)", title="Normalized duration"),
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
    # df = df.groupby(["Calendar", "SUMMARY"]).sum().reset_index()
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
