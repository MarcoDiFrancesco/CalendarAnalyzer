import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.legend import legend
from utils.remove_last_month import remove_last_month
from utils.single_activity import fill_missing_months

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
    _usage_table(df)
    st.subheader("YouTube usage")
    _bar_chart_singlecat(df, "YouTube", "red")
    st.subheader("Game usage")
    _bar_chart_singlecat(df, "Game", "#ff8000")
    st.subheader("Misc entertainment")
    _bar_chart_multicat(df)


def _bar_chart_multicat(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    # Select for debuggability
    df = df[["SUMMARY", "Period", "Duration"]]
    # Fill missing months
    df = fill_missing_months(df, "Period", "SUMMARY")
    df = df[~df["SUMMARY"].isin(["YouTube", "Game"])]
    st.write(
        alt.Chart(df)
        .mark_bar(opacity=0.9)
        .properties(width=700, height=450)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours"),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("sum(Duration)", title="Total duration (hours)"),
            ],
            color=alt.Color("SUMMARY", scale=alt.Scale(scheme="paired")),
        )
    )


def _bar_chart_singlecat(df: pd.DataFrame, category: str, color: str):
    df = df.copy()
    df = group_by_period(df, "M")
    # Select for debuggability
    df = df[["SUMMARY", "Period", "Duration"]]
    # Fill missing months
    df = fill_missing_months(df, "Period", "SUMMARY")
    df = df[df["SUMMARY"] == category]
    assert len(df) > 0, f"DataFrame does not contain {category} elements"
    st.write(
        alt.Chart(df)
        .mark_bar(opacity=0.7, color=color)
        .properties(width=650, height=400)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours"),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("sum(Duration)", title="Total duration (hours)"),
            ],
        )
    )


def _usage_table(df: pd.DataFrame) -> None:
    days_20, ent_20, yt_m_20 = _average_usage(df, 2020)
    days_21, ent_21, yt_m_21 = _average_usage(df, 2021)
    days_22, ent_22, yt_m_22 = _average_usage(df, 2022)

    table = f"""
    <table>
      <thead>
        <tr>
            <th ></th>
            <th >2020</th>
            <th >2021</th>
            <th >2022</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td >📅 Entertainment days / year</td>
            <td >{days_20/365:.0%} ({days_20} days)</td>
            <td >{days_21/365:.0%} ({days_21} days)</td>
            <td >{days_22/365:.0%} ({days_22} days)</td>
        </tr>
        <tr>
            <td >⏱ Entertainment / month</td>
            <td >{ent_20:.0f} h</td>
            <td >{ent_21:.0f} h</td>
            <td >{ent_22:.0f} h</td>
        </tr>
        <tr>
            <td >🟥 YouTube / month</td>
            <td >{yt_m_20:.0f} h</td>
            <td >{yt_m_21:.0f} h</td>
            <td >{yt_m_22:.0f} h</td>
        </tr>
        </tbody>
    </table>
    <br />
    """
    st.markdown(table, unsafe_allow_html=True)


def _average_usage(df: pd.DataFrame, year: int):
    df = df.copy()
    df = df[df["DTSTART"].dt.year == year]

    # Days per year
    tot_days = len(df["DAY"].unique())

    # Count number of months
    months_num = len(df.groupby(by=[df.DTSTART.dt.month]).sum().index)

    # Entertainment time per month
    avg_ent = df["Duration"].sum() / months_num

    # YouTube time per month
    df_yt = df[df["SUMMARY"] == "YouTube"]
    avg_yt_month = df_yt["Duration"].sum() / months_num

    return tot_days, avg_ent, avg_yt_month
