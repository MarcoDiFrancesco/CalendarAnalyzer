import pandas as pd
import altair as alt
import streamlit as st


def chart_workout(df: pd.DataFrame):
    df = df.copy()
    df = df[df["Calendar"] == "Sport"]

    for year in range(2020, 2023):
        df_year = df[df["DTSTART"].dt.year == year]
        title = f"Workout map {year}"
        chart_workout_year(df_year, title)


def chart_workout_year(df: pd.DataFrame, title: str):
    st.write(
        alt.Chart(df, title=title)
        .mark_rect()
        .encode(
            x=alt.X("date(DTSTART):O", title="Day"),
            y=alt.Y("month(DTSTART):O", title="Month", sort="-x"),
            color=alt.Color("sum(Duration):Q", scale=alt.Scale(scheme="goldorange")),
        )
        .properties(width=700)
    )
