import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import chart_calendar_vert, chart_decreasing_activity


def eat(df: pd.DataFrame) -> None:
    df = df.copy()
    st.header("Eat")
    df = remove_last_month(df, "DTSTART")
    chart_calendar_vert(df, "Eat")
    chart_decreasing_activity(df, "Eat")
    st.subheader("Meals time distribution")
    _beginning_of_day(df)


def _beginning_of_day(df: pd.DataFrame) -> None:
    df = df.copy()

    # Reindex because of duplicates given by merging muliple dataframes, one for each calendar
    df = df.reset_index()

    # Select column for debugging readability
    df = df[["Calendar", "SUMMARY", "DTSTART"]]

    # Day name e.g. Monday
    df["DayName"] = df["DTSTART"].dt.day_name()

    # Preserve original time
    df["DTSTART_Orig"] = df["DTSTART"].dt.strftime("%Y/%m/%d %H:%M")

    # Filter specific calendars
    df = df.loc[df["Calendar"].isin(["Eat"])]

    group_by = "SUMMARY"
    # TODO: write that I've done it
    df = _filter_first_daily_activity(df, group_by)

    # Add randomly + or - 15 minutes to distribute activities during the half hour
    arr_randmin = np.random.randint(-14, 15, df.shape[0])
    df_randmin = pd.DataFrame({"int": arr_randmin})
    df_randmin["time"] = pd.to_timedelta(df_randmin["int"], "min")
    df["DTSTART"] += df_randmin["time"]

    # Extract time from start date
    df["DTSTART_AltForm"] = df["DTSTART"].dt.strftime("%Y/%m/%d %H:%M")

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
                "hoursminutes(DTSTART_AltForm):T",
                title=None,
                scale=alt.Scale(domain=["2012-01-01T00:00:00", "2012-01-02T01:00:00"]),
            ),
            tooltip=[
                alt.Tooltip("Calendar"),
                alt.Tooltip("SUMMARY", title="Activity"),
                alt.Tooltip("yearmonthdatehoursminutes(DTSTART_Orig)", title="Date"),
            ],
            color=alt.Color(f"{group_by}:N", legend=None),
            column=alt.Column(
                "DayName:N",
                title=None,
                header=alt.Header(
                    labelFontSize=16,
                    labelAngle=0,
                    titleOrient="top",
                    labelOrient="bottom",
                    labelAlign="center",
                ),
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


def _filter_first_daily_activity(df: pd.DataFrame, group_by: str) -> pd.DataFrame:
    """Get first activity per each day, for each calendar."""

    # e.g. Calendar: Eat, SUMMARY: Breakfast
    assert group_by in ["Calendar", "SUMMARY"]

    # Group by day and Calendar
    df["DTSTART_tmp"] = df["DTSTART"]
    df = df.set_index(["DTSTART_tmp", group_by])
    df = df.groupby(
        [pd.Grouper(level="DTSTART_tmp", freq="24h"), pd.Grouper(level=group_by)]
    ).first()
    df = df.reset_index()

    # Drop column that now contains dates like 2019-12-01
    df = df.drop("DTSTART_tmp", axis=1)
    return df
