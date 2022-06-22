import altair as alt
import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def chores(df: pd.DataFrame) -> None:
    df = df.copy()
    st.header("Chores")
    st.markdown(
        """
        Observations:
        - Spike beginning of 2022: I chose the university and organized courses
        """
    )
    df = remove_last_month(df, "DTSTART")
    df = df.loc[df["Calendar"] == "Chores"]
    _chart_calendar_vert(df)


def _chart_calendar_vert(df: pd.DataFrame):
    df = filter_df_chart(df, "Chores")
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
