import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.legend import legend
from utils.normalize import normalize_all_to_one
from utils.remove_last_month import remove_last_month


def chart_calendars(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalize_all_to_one(df)
    df = remove_last_month(df, "Period")
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(height=500)
        .encode(
            x=alt.X("Period", title="Month"),
            y=alt.Y(
                "sum(Duration)", title="Normalized duration", axis=alt.Axis(format="%")
            ),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
    )


def chart_calendars_longest(df: pd.DataFrame):
    st.subheader("Longest non-stop activities")
    df = df.copy()
    df = df.sort_values("Duration", ascending=False)
    df = df.drop_duplicates("SUMMARY")
    df = df.head(10)
    st.altair_chart(
        alt.Chart(df)
        .mark_bar(point=True)
        .properties(width=700, height=300)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y("SUMMARY", title="Activity", sort="-x"),
            color=alt.Color("Calendar", scale=legend(df)),
            tooltip=[
                alt.Tooltip("Duration", title="Duration (hours)"),
                alt.Tooltip("yearmonthdatehoursminutes(DTSTART)", title="Start date"),
                alt.Tooltip("yearmonthdatehoursminutes(DTEND)", title="End date"),
            ],
        )
    )


def time_quality(df: pd.DataFrame) -> None:
    st.subheader("Time quality")
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalize_all_to_one(df)
    df = remove_last_month(df, "Period")

    act_bad = ["Chores", "Commute", "Eat", "Entertainment", "Personal care"]
    df_bad = df.loc[df["Calendar"].isin(act_bad)]
    left = (
        alt.Chart(df_bad)
        .encode(
            y=alt.Y("Period:O", axis=None),
            x=alt.X("Duration", title="hourss", sort=alt.SortOrder("descending")),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
        .mark_bar()
        .properties(title="Bad", width=250)
    )
    middle = (
        alt.Chart(df)
        .encode(
            y=alt.Y("Period", axis=None),
            text=alt.Text("Period"),
        )
        .mark_text()
        .properties(width=50)
    )
    act_good = ["Personal development", "Spare time", "Sport", "Study", "Work"]
    df_good = df.loc[df["Calendar"].isin(act_good)]
    right = (
        alt.Chart(df_good)
        .encode(
            y=alt.Y("Period:O", axis=None),
            x=alt.X("Duration", title="hourss"),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
            tooltip=[
                "Calendar",
                alt.Tooltip("sum(Duration)", title="Monthly occupation", format=".1%"),
            ],
        )
        .mark_bar()
        .properties(title="Good", width=250)
    )
    st.altair_chart(alt.concat(left, middle, right, spacing=5))


def beginning_of_day(df: pd.DataFrame) -> None:
    df = df.copy()
    # Reindex because of duplicates given by merging muliple dataframes, one for
    # each calendar
    df = df.reset_index()

    # Select only specific calendars
    # df = df.loc[df["Calendar"].isin(["Eat", "Study"])]

    # Select column for debugging readability
    df = df[["Calendar", "SUMMARY", "DTSTART"]]
    df["DayName"] = df["DTSTART"].dt.day_name()

    # Add randomly + or - 15 minutes to distribute activities during the half hour
    # TODO: undestand why adding few seconds change completely the plot
    arr_randmin = np.random.randint(0, 1, df.shape[0])
    df_randmin = pd.DataFrame({"int": arr_randmin})
    df_randmin["time"] = pd.to_timedelta(df_randmin["int"], "sec")
    df["DTSTART"] += df_randmin["time"]

    # Extract time from start date
    df["Time"] = df["DTSTART"].dt.time

    # df = df.loc[df["Calendar"].isin(["Eat"])]

    # TODO: undestand why half hours are not shown

    print(df)
    st.altair_chart(
        alt.Chart(df)
        .mark_circle(size=14)
        .encode(
            x=alt.X(
                "jitter:Q",
                title=None,
                axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
                scale=alt.Scale(),
            ),
            y=alt.Y(
                "hoursminutes(Time):T",
                # scale=alt.Scale(domain=["2012-01-01T04:00:00", "2012-01-02T04:00:00"]),
                scale=alt.Scale(domain=["2012-01-01T00:00:00", "2012-01-02T00:00:00"]),
            ),
            tooltip=[
                alt.Tooltip("Calendar"),
                alt.Tooltip("SUMMARY", title="Activity"),
                # TODO: set to minutesseconds
                alt.Tooltip("yearmonthdatehoursminutesseconds(Time)"),
            ],
            color=alt.Color("DayName:N", legend=None),
            column=alt.Column(
                "DayName:N",
                header=alt.Header(
                    labelFontSize=16,
                    labelAngle=0,
                    titleOrient="top",
                    labelOrient="bottom",
                    labelAlign="center",
                    labelPadding=25,
                ),
            ),
        )
        .transform_calculate(
            # Generate Gaussian jitter with a Box-Muller transform
            jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
        )
        .configure_facet(spacing=0)
        .configure_view(stroke=None)
        .configure_axis(labelFontSize=16, titleFontSize=16)
        .properties(height=400, width=85)
    )
