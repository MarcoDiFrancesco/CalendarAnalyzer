import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.legend import legend
from utils.remove_last_month import remove_last_month


def personal_development(df: pd.DataFrame):
    df = df.copy()
    st.markdown("---")
    st.header("Personal Development")
    _layered_bar_chart(df)
    st.subheader("Fiddling vs Working on projects")
    _fiddle_plot(df)
    st.subheader("Personal projects")
    _projects_plot(df)


def _fiddle_plot(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = df.loc[df["Calendar"] == "Personal development"]
    df.loc[df["SUMMARY"] == "Linux", "Category"] = "Linux"
    df.loc[df["SUMMARY"] != "Linux", "Category"] = "Learn-Projects"
    # Show in front Non-Fiddle (the most important)
    df = df.sort_values(["Period", "Category"], ascending=False)
    # Horizotal chart does not require last month to be removed
    df = remove_last_month(df, "Period")
    print("FIDDLEEE", df)
    st.altair_chart(
        alt.Chart(df)
        .mark_bar(opacity=0.75)
        .properties(width=700, height=500)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours", stack=None),
            color=alt.Color(
                "Category",
                legend=alt.Legend(title="Activity"),
                scale=legend(
                    df,
                    color_map={"Linux": "#B39DDB", "Learn-Projects": "#fcc221"},
                    column="Category",
                ),
            ),
            tooltip=[
                alt.Tooltip("Category", title="Activity"),
                alt.Tooltip("sum(Duration)", title="Total duration (hours)"),
            ],
        )
        .configure_legend(labelLimit=120),
    )


def _projects_plot(df: pd.DataFrame):
    df = df.copy()
    df = remove_last_month(df, "DTSTART")
    df = df.loc[df["Calendar"] == "Personal development"]
    df = df.loc[df["SUMMARY"] != "Linux"]
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


def _layered_bar_chart(df: pd.DataFrame):
    df = df.copy()
    df["Period"] = df["DTSTART"].dt.day_name()
    df = df.loc[
        (df["Calendar"] == "Personal development") | (df["Calendar"] == "Study")
    ]
    df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df["Duration"] /= df["Duration"].max()
    chart = (
        alt.Chart(df)
        .mark_bar(opacity=0.5)
        .properties(width=60, height=300)
        .encode(
            x=alt.X("Calendar", title="", axis=alt.Axis(labels=False)),
            y=alt.Y("Duration:Q", title="Ratio", axis=alt.Axis(format="%")),
            column=alt.Column(
                "Period:O",
                title="Day of the week",
                sort=[
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
            ),
            tooltip=[
                alt.Tooltip(
                    "Period",
                    title="Day",
                ),
                alt.Tooltip(
                    "Duration",
                    title="Ratio",
                    format=".0%",
                ),
            ],
            color=alt.Color("Calendar", scale=legend(df)),
        )
    )
    st.altair_chart(chart)
