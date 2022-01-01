import pandas as pd
import altair as alt
import streamlit as st
from utils.remove_last_month import remove_last_month


def chart_workout(df: pd.DataFrame):
    df = df.copy()
    df = remove_last_month(df, "DTSTART")
    df = df[df["Calendar"] == "Sport"]

    for year in range(2020, 2023):
        st.subheader(f"Stats {year}")
        df_year = df[df["DTSTART"].dt.year == year]
        _stats(df_year)
        title = f"Workout map {year}"
        _chart_workout_year(df_year, title)


def _stats(df: pd.DataFrame):
    tot_days = len(df["DAY"].unique())
    st.write(f"**Total days**: {tot_days}")


def _chart_workout_year(df: pd.DataFrame, title: str):
    st.write(
        alt.Chart(df, title=title)
        .mark_rect()
        .encode(
            x=alt.X("date(DTSTART):O", title="Day"),
            y=alt.Y("month(DTSTART):O", title="Month"),
            color=alt.Color("sum(Duration):Q", scale=alt.Scale(scheme="goldorange")),
        )
        .properties(width=700)
    )
