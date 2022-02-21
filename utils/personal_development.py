import pandas as pd
import streamlit as st
import altair as alt
from utils.normalize import normalize_to_average, normalized_duration
from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart
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
    df["Duration"] *= 100
    print(df)
    chart = (
        alt.Chart(df)
        .mark_bar(opacity=0.5)
        .properties(width=700, height=300)
        .encode(
            x=alt.X(
                "Period:O",
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
            y=alt.Y("Duration:Q", title="Ratio", stack=None),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
        )
    )
    st.altair_chart(chart)
