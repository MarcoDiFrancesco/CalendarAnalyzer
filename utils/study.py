import pandas as pd
import altair as alt
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


def rige_plot(df: pd.DataFrame):
    # from vega_datasets import data

    # source = data.seattle_weather.url

    # step = 20
    # overlap = 1

    # chart = (
    #     alt.Chart(source, height=step)
    #     .transform_timeunit(Month="month(date)")
    #     .transform_joinaggregate(mean_temp="mean(temp_max)", groupby=["Month"])
    #     .transform_bin(["bin_max", "bin_min"], "temp_max")
    #     .transform_aggregate(
    #         value="count()", groupby=["Month", "mean_temp", "bin_min", "bin_max"]
    #     )
    #     .transform_impute(
    #         impute="value", groupby=["Month", "mean_temp"], key="bin_min", value=0
    #     )
    #     .mark_area(
    #         interpolate="monotone", fillOpacity=0.8, stroke="lightgray", strokeWidth=0.5
    #     )
    #     .encode(
    #         alt.X("bin_min:Q", bin="binned", title="Maximum Daily Temperature (C)"),
    #         alt.Y("value:Q", scale=alt.Scale(range=[step, -step * overlap]), axis=None),
    #         alt.Fill(
    #             "mean_temp:Q",
    #             legend=None,
    #             scale=alt.Scale(domain=[30, 5], scheme="redyellowblue"),
    #         ),
    #     )
    #     .facet(
    #         row=alt.Row(
    #             "Month:T",
    #             title=None,
    #             header=alt.Header(labelAngle=0, labelAlign="right", format="%B"),
    #         )
    #     )
    #     .properties(title="Seattle Weather", bounds="flush")
    #     .configure_facet(spacing=0)
    #     .configure_view(stroke=None)
    #     .configure_title(anchor="end")
    # )
    st.write(chart)
