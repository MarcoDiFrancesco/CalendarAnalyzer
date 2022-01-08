import pandas as pd
import altair as alt
import streamlit as st
from utils.normalize import normalize_max_to_one, normalized_duration
from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def chart_study_vert(df: pd.DataFrame):
    st.markdown(
        """
        ### Trend of study during time
        - normalized to 1
        - last month's data is removed
        """
    )
    df = filter_df_chart(df, "Study")
    df = normalized_duration(df)
    df = remove_last_month(df, "Period")
    df = normalize_max_to_one(df)
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=350)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours"),
        )
        .configure_legend(labelLimit=120)
    )


def chart_study_horiz(df: pd.DataFrame):
    df = filter_df_chart(df, "Study")
    df = df.groupby(["SUMMARY"]).sum().reset_index()
    # Round to closes integer
    df = df.round(0)
    bars = (
        alt.Chart(df)
        .mark_bar(point=True)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y(
                "SUMMARY",
                title="Activity",
                sort="-x",
                # axis=alt.Axis(domain=False, tickSize=0, labelPadding=10),
            ),
            color=alt.Color("SUMMARY", legend=None),
        )
    )
    text = bars.mark_text(
        align="left",
        baseline="middle",
        dx=3,  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(text="Duration:Q")
    chart = (bars + text).properties(padding={"right": 10}, width=600, height=500)
    st.write(chart)
