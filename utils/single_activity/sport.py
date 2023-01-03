import altair as alt
import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def sport(df: pd.DataFrame):
    st.markdown("---")
    st.header("Sport")
    df = df.copy()
    df = remove_last_month(df, "DTSTART")
    df = df[df["Calendar"] == "Sport"]

    # Compute days
    df_year = df[df["DTSTART"].dt.year == 2020]
    days_20 = len(df_year["DAY"].unique())
    df_year = df[df["DTSTART"].dt.year == 2021]
    days_21 = len(df_year["DAY"].unique())
    df_year = df[df["DTSTART"].dt.year == 2022]
    days_22 = len(df_year["DAY"].unique())

    # Show table
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
            <td >📅 Sport days</td>
            <td >{days_20/365:.0%} ({days_20} days)</td>
            <td >{days_21/365:.0%} ({days_21} days)</td>
            <td >{days_22/365:.0%} ({days_22} days)</td>
        </tr>
        </tbody>
    </table>
    <br />
    """
    st.markdown(table, unsafe_allow_html=True)

    _vertical(df)

    # Observations
    st.markdown(
        """
        Observations:
        - During winter 2020, right before the lockdown I skied a lot, compared to winter 2021 in lockdown
        - During the first summer session of 2021 I played for a while beach volley, in summer 2020 I did nothing in that period, but I passed a lot of exams
        """
    )

    # Heat maps
    for year in range(2020, 2023):
        df_year = df[df["DTSTART"].dt.year == year]
        title = f"Sport map {year}"
        _heat_map(df_year, title, color_scheme="goldgreen")


def _vertical(df: pd.DataFrame):
    df = filter_df_chart(df, "Sport")
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


def _heat_map(df: pd.DataFrame, title: str, color_scheme):
    st.write(
        alt.Chart(df, title=title)
        .mark_rect(opacity=0.9)
        .encode(
            x=alt.X("date(DTSTART):O", title="Day"),
            y=alt.Y("month(DTSTART):O", title="Month"),
            color=alt.Color(
                "sum(Duration):Q", title="Hours", scale=alt.Scale(scheme=color_scheme)
            ),
            tooltip=[
                alt.Tooltip("sum(Duration):Q", title="Hours"),
            ],
        )
        .properties(width=700)
    )
