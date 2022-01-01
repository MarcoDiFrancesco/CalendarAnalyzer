import warnings

import altair as alt
import pandas as pd
import streamlit as st
from streamlit.commands.page_config import set_page_config

from utils import clean_df, admin
from utils.download_cals import download_cals
from utils.table_sum import table_sum
from utils.remove_last_month import remove_last_month
from utils.normalize import normalize_to_one, normalized_duration
from utils.legend import legend
from utils.fix_activitires import fix_activities
from utils.compute_day import compute_day
from utils.sport import chart_sport
from utils.entertainment import entertainment
from utils.group_by_period import group_by_period
from utils.single_activity import (
    chart_calendar,
    chart_decreasing_activity,
    select_activity,
)


def chart_calendars(df: pd.DataFrame):
    df = df.copy()
    df = group_by_period(df, "M")
    df = df = df.groupby(["Period", "Calendar"]).sum().reset_index()
    df = normalized_duration(df)
    df = normalize_to_one(df)
    df = remove_last_month(df)
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=500)
        .encode(
            x=alt.X("Period", title="Month"),
            y=alt.Y("sum(Duration)", title="Normalized duration"),
            color=alt.Color(
                "Calendar",
                scale=legend(df),
                legend=alt.Legend(title="Calendar"),
            ),
        )
    )


def chart_calendars_longest(df: pd.DataFrame):
    st.subheader("Longest non-stop activities")
    df = df.copy()
    # df = df.groupby(["Calendar", "SUMMARY"]).sum().reset_index()
    df = df.sort_values("Duration", ascending=False)
    df = df.drop_duplicates("SUMMARY")
    df = df.head(10)
    st.write(
        alt.Chart(df)
        .mark_bar(point=True)
        .properties(width=700, height=300)
        .encode(
            alt.X("Duration", title="Hours"),
            alt.Y("SUMMARY", title="Activity", sort="-x"),
            color=alt.Color("Calendar", scale=legend(df)),
        )
    )


set_page_config(page_title="Calendar Analyzer", page_icon="⌛")
st.title("Calendar Analyzer")
st.caption(
    "[https://github.com/MarcoDiFrancesco/CalendarAnalyzer](https://github.com/MarcoDiFrancesco/CalendarAnalyzer)"
)

df = download_cals().copy()
df = clean_df.clean_df(df)

df = admin.get_password(df)
df = df.sort_values("DTSTART")
compute_day(df)
fix_activities(df)

# All activities
st.markdown("---")
st.header("All activities")
chart_calendars(df)
chart_calendars_longest(df)
table_sum(df)

# Selected activity
st.markdown("---")
st.header("Single activity")
st.text("Unique activities divided by calendar")
calendar = select_activity(df)
chart_calendar(df, calendar)
chart_decreasing_activity(df, calendar)
table_sum(df, calendar)

# Workout
st.markdown("---")
st.header("Sport")
chart_sport(df)
entertainment(df)
