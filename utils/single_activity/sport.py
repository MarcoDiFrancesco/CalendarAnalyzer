import altair as alt
import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import chart_calendar_vert


def sport(df: pd.DataFrame):
    st.markdown("---")
    st.header("Sport")
    df = df.copy()
    df = remove_last_month(df, "DTSTART")
    df = df[df["Calendar"] == "Sport"]

    for year in range(2020, 2022):
        df_year = df[df["DTSTART"].dt.year == year]
        tot_days = len(df_year["DAY"].unique())
        st.text(f"Sport days of {year}: {tot_days}/365 ({tot_days/365:.0%})")

    chart_calendar_vert(df, "Sport")

    for year in range(2020, 2023):
        df_year = df[df["DTSTART"].dt.year == year]
        title = f"Sport map {year}"
        _heat_map(df_year, title, color_scheme="goldgreen")


def _heat_map(df: pd.DataFrame, title: str, color_scheme):
    st.write(
        alt.Chart(df, title=title)
        .mark_rect()
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
