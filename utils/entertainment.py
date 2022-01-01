import streamlit as st
import pandas as pd
from utils.workout import heat_map
import altair as alt
from utils.group_by_period import group_by_period
from utils.legend import legend

color_map = {
    "YouTube": "#F4511E",
}


def entertainment(df: pd.DataFrame):
    df = df.copy()
    st.header("Entertainment")
    df = df[df["Calendar"] == "Entertainment"]
    _average_usage(df, 2021)
    _bar_chart(df)


def _average_usage(df: pd.DataFrame, year: int):
    df = df.copy()
    df = df[df["DTSTART"].dt.year == year]
    st.subheader(f"Year {year}")
    tot_days = len(df["DAY"].unique())
    st.text(f"Days: {tot_days}/{365}")
    avg_by_month = df["Duration"].sum() / 12
    st.text(f"Average time spent per month: {avg_by_month:.2f} hours")
    avg_session = df["Duration"].mean()
    st.text(f"Average session lenght: {avg_session:.2f} hours")


def _bar_chart(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    st.write(
        alt.Chart(df, title="YouTube usage")
        .mark_bar()
        .properties(width=700, height=400)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours"),
            color=alt.Color(
                "SUMMARY",
                # scale=legend(df, color_map, "SUMMARY"),
                legend=alt.Legend(title="Activity"),
            ),
        )
    )
