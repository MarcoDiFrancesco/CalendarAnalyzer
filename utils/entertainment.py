import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.legend import legend
from utils.remove_last_month import remove_last_month

color_map = {
    "YouTube": "#F4511E",
}


def entertainment(df: pd.DataFrame):
    df = df.copy()
    st.header("Entertainment")
    df = remove_last_month(df, "DTSTART")
    df = df[df["Calendar"] == "Entertainment"]
    st.markdown(
        """
        Observations:
        - Days I used to entertain myself incresed
        - I played Stardew Valley during winter session of 2021 replacing the time spent YouTube, it's a sign that one balanced the other
        - I decreased my average entertainment and YouTube time gaming a little bit less
        - Starting from December and through the whole winter session I entertain myself a lot,
          maybe this is due to me going back to my parents' home where the organizational strees increases
        - September to November is where I'm entertaining myself the least
        - YouTube activities are becoming shorter. This may be due to YouTube Shorts.
        """
    )
    _average_usage(df, 2020)
    _average_usage(df, 2021)
    _bar_chart(df)


def _average_usage(df: pd.DataFrame, year: int):
    df = df.copy()
    df = df[df["DTSTART"].dt.year == year]
    st.subheader(f"Year {year}")
    # Days per year
    tot_days = len(df["DAY"].unique())
    st.text(f"📅 Days of usage: {tot_days}/{365}")
    # Entertainment time per month
    avg_ent = df["Duration"].sum() / 12
    st.text(f"⏱ Average entertainment time per month: {avg_ent:.1f} hours")
    # YouTube time per month
    df_yt = df[df["SUMMARY"] == "YouTube"]
    avg_yt_month = df_yt["Duration"].sum() / 12
    st.text(f"🟥 Average YouTube time per month: {avg_yt_month:.1f} hours")
    # Average session lenght
    avg_yt_session = df_yt["Duration"].mean()
    st.text(f"⏳ Average YouTube session lenght: {avg_yt_session:.2f} hours")


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
