import altair as alt
import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def personal_care(df: pd.DataFrame) -> None:
    """Removed category due to luck of data meaning.

    Details: https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/94
    """
    df = df.copy()
    st.header("Personal care")
    df = remove_last_month(df, "DTSTART")
    _chart_calendar_vert(df)
    _chart_decreasing_activity(df)


def _chart_calendar_vert(df: pd.DataFrame):
    df = filter_df_chart(df, "Personal care")
    # Horizotal chart does not require last month to be removed
    df = remove_last_month(df, "Period")

    st.altair_chart(
        alt.Chart(df)
        .mark_bar()
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


def _chart_decreasing_activity(df: pd.DataFrame):
    df = df.copy()
    df = df.loc[df["Calendar"] == "Personal care"]
    df = df.groupby(["SUMMARY"]).sum().reset_index()
    st.write(
        alt.Chart(df)
        .mark_bar(point=True)
        .properties(width=550, height=500)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y("SUMMARY", title="Activity", sort="-x"),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("Duration", title="Total duration (hours)", format=".0f"),
            ],
            color=alt.Color("SUMMARY", legend=None),
        )
    )
