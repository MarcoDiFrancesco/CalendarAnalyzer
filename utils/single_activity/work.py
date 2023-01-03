import altair as alt
import pandas as pd
import streamlit as st

from utils.fill_month_values import fill_month_values
from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def work(df: pd.DataFrame) -> None:
    df = df.copy()
    df = df[df["Calendar"] == "Work"]
    if not len(df.index):
        return
    st.header("Work")
    # df = remove_last_month(df, "DTSTART")
    _chart_calendar_vert(df)


def _chart_calendar_vert(df: pd.DataFrame):
    df = filter_df_chart(df, "Work")

    df = fill_month_values(df, "Period", "Duration")

    # Fill month sets SUMMARY as nan, so replace this value (set as 0) with something
    df.fillna("FBK", inplace=True)

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


# def _chart_decreasing_activity(df: pd.DataFrame, calendar: str):
#     df = df.copy()
#     df = df.loc[df["Calendar"] == calendar]
#     df = df.groupby(["SUMMARY"]).sum().reset_index()
#     st.write(
#         alt.Chart(df)
#         .mark_bar(point=True, opacity=0.9)
#         .properties(width=550, height=350)
#         .encode(
#             alt.X("Duration", title="Hours"),
#             alt.Y("SUMMARY", title="Activity", sort="-x"),
#             tooltip=[
#                 alt.Tooltip("SUMMARY", title="Activity"),
#                 alt.Tooltip("Duration", title="Total duration (hours)", format=".0f"),
#             ],
#             color=alt.Color("SUMMARY", legend=None),
#         )
#     )
