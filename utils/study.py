from os import name

import altair as alt
import pandas as pd
import streamlit as st

from utils.normalize import normalize_to_average, normalized_duration
from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def study(df: pd.DataFrame):
    st.markdown("---")
    st.header("Study")
    chart_vert(df)
    chart_horiz(df)
    rige_plot(df)


def chart_vert(df: pd.DataFrame):
    st.markdown(
        """
        ### Trend of study during time
        - Normalized to average duration
        - Last month's data is removed
        """
    )
    df = filter_df_chart(df, "Study")
    df = normalized_duration(df)
    df = remove_last_month(df, "Period")
    df = normalize_to_average(df)
    bars = (
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=350)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Ratio"),
            tooltip=[
                alt.Tooltip("sum(Duration)", title="Ratio", format=".0%"),
            ],
        )
    )
    line = (
        alt.Chart(pd.DataFrame({"y": [1]}))
        .mark_rule(color="firebrick")
        .encode(y="y", size=alt.SizeValue(2))
    )
    st.write(alt.layer(bars, line))


def chart_horiz(df: pd.DataFrame):
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
    line = bars.mark_text(
        align="left",
        baseline="middle",
        dx=3,  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(text="Duration:Q")

    chart = alt.layer(bars, line).properties(
        padding={"right": 10}, width=600, height=500
    )
    st.write(chart)


def _add_zeros(df):
    """Add zeros if not studied a subject month"""
    df = df.groupby(["Period", "SUMMARY"]).sum()
    df = pd.pivot_table(
        df, index="Period", columns="SUMMARY", values="Duration", fill_value=0
    )
    df = df.reset_index()
    df = df.melt("Period", var_name="SUMMARY", value_name="Duration")
    return df


def _order_subjects(df: pd.DataFrame) -> list:
    """Order subjects by peak date
    Return list ordered list of subjects
    """
    # Get rows with max value of Duration
    df_peak = df.loc[df.groupby(["SUMMARY"])["Duration"].idxmax()]
    df_peak = df_peak.sort_values("Period")
    list_peak = df_peak["SUMMARY"].tolist()
    return list_peak


def rige_plot(df: pd.DataFrame):
    step = 20  # Height of the each area plot
    overlap = 1  # Height of the area

    df = filter_df_chart(df, "Study")
    df = normalized_duration(df)
    df = remove_last_month(df, "Period")
    df = _add_zeros(df)
    subjects_order = _order_subjects(df)
    # Replace this color color by subject
    df["color"] = df["Duration"].apply(lambda d: "blue" if d < 10 else "red")
    chart = (
        alt.Chart(df, height=step)
        .transform_joinaggregate(mean_temp="mean(Duration)", groupby=["SUMMARY"])
        .mark_area(
            interpolate="monotone", fillOpacity=0.8, stroke="lightgray", strokeWidth=0.5
        )
        .encode(
            alt.X("Period:O", bin="binned", title=None),
            alt.Y(
                "Duration:Q", scale=alt.Scale(range=[step, -step * overlap]), axis=None
            ),
            tooltip=[
                alt.Tooltip(
                    "Duration",
                    title="Studied hours (month)",
                    format=".2",
                ),
                alt.Tooltip(
                    "SUMMARY",
                    title="Subject",
                    # format=".2",
                ),
            ]
            # TODO: add color palette like here https://stackoverflow.com/a/65861410/7924557
            # TODO: find a color scheme that makes sense, maybe join study with personal dev
            #       and color in yellow the projects? Then there is the problem of linux project
            #       and anyway most projects are very little, so not noticible
            # alt.Fill(
            #     "color:O",
            #     # legend=None,
            #     scale=None,
            # ),
        )
        .facet(
            row=alt.Row(
                "SUMMARY:O",
                title="Subject",
                header=alt.Header(labelAngle=0, labelAlign="left"),
                sort=subjects_order,
            )
        )
        .properties(title="Subject study distribution by month", bounds="flush")
        .configure_facet(spacing=0)
        .configure_view(stroke=None)
        .configure_title(anchor="middle")
    )
    st.altair_chart(chart)
