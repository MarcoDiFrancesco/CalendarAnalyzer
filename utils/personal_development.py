import altair as alt
import pandas as pd
import streamlit as st

from utils.legend import legend


def personal_development(df: pd.DataFrame):
    df = df.copy()
    st.markdown("---")
    st.header("Personal Development")
    layered_bar_chart(df)


def layered_bar_chart(df: pd.DataFrame):
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
            y=alt.Y("Duration:Q", title="Ratio"),
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
