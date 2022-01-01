import pandas as pd
import altair as alt
import streamlit as st
from utils.remove_last_month import remove_last_month


def chart_workout(df: pd.DataFrame):
    df = df.copy()
    df = remove_last_month(df, "DTSTART")
    df = df[df["Calendar"] == "Sport"]

    for year in range(2020, 2023):
        df_year = df[df["DTSTART"].dt.year == year]
        tot_days = len(df_year["DAY"].unique())
        st.text(f"Workout days of {year}: {tot_days}/365")

    for year in range(2020, 2023):
        df_year = df[df["DTSTART"].dt.year == year]
        title = f"Workout map {year}"
        heat_map(df_year, title, color_scheme="goldgreen")


def heat_map(df: pd.DataFrame, title: str, color_scheme):
    st.write(
        alt.Chart(df, title=title)
        .mark_rect()
        .encode(
            x=alt.X("date(DTSTART):O", title="Day"),
            y=alt.Y("month(DTSTART):O", title="Month"),
            color=alt.Color("sum(Duration):Q", scale=alt.Scale(scheme=color_scheme)),
        )
        .properties(width=700)
    )
