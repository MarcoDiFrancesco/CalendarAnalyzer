import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.remove_last_month import remove_last_month


def single_activity_text(df: pd.DataFrame):
    act_tot = len(df.index)
    st.markdown(
        f"""
        ---
        # Single activity

        - {act_tot} activities in total over 2 and a half years
        """
    )


def filter_df_chart(df: pd.DataFrame, calendar: str):
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = df.loc[df["Calendar"] == calendar]
    return df


def chart_calendar_vert(df: pd.DataFrame, calendar: str):
    # TODO: remove this function (above) once all categories are splitted
    df = filter_df_chart(df, calendar)
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


def chart_decreasing_activity(df: pd.DataFrame, calendar: str):
    # TODO: remove this function (above) once all categories are splitted
    df = df.copy()
    df = df.loc[df["Calendar"] == calendar]
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
