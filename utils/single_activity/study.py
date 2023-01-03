import altair as alt
import pandas as pd
import streamlit as st

from utils.data_checks.check_name import study_subjects
from utils.df_shorten_string import df_shorten_string
from utils.fill_month_values import fill_month_values
from utils.normalize import normalize_to_average, normalized_duration
from utils.remove_last_month import remove_last_month
from utils.single_activity import filter_df_chart


def study(df: pd.DataFrame) -> None:
    st.markdown("---")
    st.header("Study")
    chart_vert(df)
    chart_horiz(df)
    ridge_plot(df)


def chart_vert(df: pd.DataFrame) -> None:
    st.markdown(
        """
        ### Trend
        """
    )
    df = filter_df_chart(df, "Study")
    df = normalized_duration(df)
    df = normalize_to_average(df)
    df = df.groupby(["Period"]).sum()
    df = df.reset_index()
    df = fill_month_values(df, "Period", "Duration")
    df = remove_last_month(df, "Period")

    # Relative duration from 100%
    # e.g. 67% -> -34%, 111% -> 11%
    df["RelativeDuration"] = df["Duration"] - 1
    bars = (
        alt.Chart(df)
        .mark_bar(opacity=0.9)
        .properties(width=670, height=350)
        .encode(
            x=alt.X("Period"),
            y=alt.Y("Duration", title="Study", axis=alt.Axis(format="%")),
            tooltip=[
                alt.Tooltip(
                    "RelativeDuration",
                    title="Deviation from the average",
                    format="+.0%",
                ),
            ],
        )
    )
    line = (
        alt.Chart(pd.DataFrame({"y": [1]}))
        .mark_rule(color="firebrick")
        .encode(y="y", size=alt.SizeValue(2))
    )
    st.write(alt.layer(bars, line))
    # st.write(bars)


def chart_horiz(df: pd.DataFrame):
    st.markdown(
        """
        ### Time cost per exam
        """
    )
    df = filter_df_chart(df, "Study")
    df = df.groupby(["SUMMARY"]).sum().reset_index()
    subjects = study_subjects()
    chart_horiz_single(df, subjects["Bachelor"])
    chart_horiz_single(df, subjects["Master"])
    chart_horiz_single(df, subjects["Other"])


def chart_horiz_single(df: pd.DataFrame, subjects: list):
    df = df_shorten_string(df, "SUMMARY")
    df = df[df["SUMMARY"].isin(subjects)]

    # Round to closes integer
    df = df.round(0)
    bars = (
        alt.Chart(df)
        .mark_bar(point=True, opacity=0.9)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y(
                "SUMMARY",
                title="Activity",
                sort="-x",
                # axis=alt.Axis(domain=False, tickSize=0, labelPadding=10),
            ),
            tooltip=[
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("Duration", title="Total duration (hours)"),
            ],
            color=alt.Color("SUMMARY", legend=None),
        )
        .properties()
    )
    line = bars.mark_text(
        align="left",
        baseline="middle",
        dx=3,  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(text="Duration:Q")

    # Height depending on number of subjects
    height = 100 + len(subjects) * 25

    chart = alt.layer(bars, line).properties(
        padding={"right": 10}, width=650, height=height
    )
    st.write(chart)


def _add_zeros(df):
    """Add zeros if not studied a subject month."""
    df = df.groupby(["Period", "SUMMARY"]).sum()
    df = pd.pivot_table(
        df, index="Period", columns="SUMMARY", values="Duration", fill_value=0
    )
    df = df.reset_index()
    df = df.melt("Period", var_name="SUMMARY", value_name="Duration")
    return df


def _order_subjects(df: pd.DataFrame) -> list:
    """Order subjects by peak date.

    Return list ordered list of subjects
    """
    # Get rows with max value of Duration
    df_peak = df.loc[df.groupby(["SUMMARY"])["Duration"].idxmax()]
    df_peak = df_peak.sort_values("Period")
    list_peak = df_peak["SUMMARY"].tolist()
    return list_peak


def ridge_plot(df: pd.DataFrame):

    st.markdown(
        """
        ### Study distribution by subject
        """
    )

    step = 20  # Height of each area plot
    overlap = 1  # Height of the area

    df = filter_df_chart(df, "Study")
    df = df_shorten_string(df, "SUMMARY")
    df = normalized_duration(df)
    df = remove_last_month(df, "Period")
    df = _add_zeros(df)
    subjects_order = _order_subjects(df)
    month_count = len(df.Period.unique())
    # Replace this color by subject
    df["color"] = df["Duration"].apply(lambda d: "blue" if d < 10 else "red")
    chart = (
        alt.Chart(df, height=step, width={"step": 0.47 * month_count})
        .transform_joinaggregate(mean_temp="mean(Duration)", groupby=["SUMMARY"])
        .mark_area(
            interpolate="monotone",
            fillOpacity=0.8,
            stroke="lightgray",
            strokeWidth=0.5,
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
            ],
        )
        .facet(
            row=alt.Row(
                "SUMMARY:O",
                title="Subject",
                header=alt.Header(labelAngle=0, labelAlign="left"),
                sort=subjects_order,
            )
        )
        .properties(title="", bounds="flush")
        .configure_facet(spacing=0)
        .configure_view(stroke=None)
        .configure_title(anchor="middle")
    )

    st.altair_chart(chart)
