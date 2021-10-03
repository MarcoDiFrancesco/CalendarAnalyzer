import os
from utils.Calendar import Calendar
import streamlit as st
import altair as alt
import logging
from utils.table_sd_sum import table_sd_sum
from utils.show_checkboxes import show_checkboxes
import pandas as pd
import datetime


def get_password():
    """Return true if password is correct"""
    password = st.text_input("Enter a password", type="password")
    if os.environ.get("DEBUG"):
        return True
    if password == os.environ.get("PSW"):
        return True
    return False


def show_group_by():
    # Show radio options horizontally
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )
    return st.radio("Group by", options=["Month", "Week"])


def select_activity(calendar):
    cal_list = calendar.calendars["Activity"].unique()
    return st.selectbox("List of all calendars", cal_list)


def show_filter(calendar, group_by):
    # Filter section
    filter = st.expander("Filters")
    with filter:
        st.write("TO IMPLEMENT")
        if not get_password():
            return True
        start, stop = st.select_slider(
            "Restrict period",
            ["01/20", "02/20", "03/20"],
            value=("01/20", "02/20"),
        )


def get_df(calendar: Calendar, group_by: str, fm, sel_cal=None):
    if group_by == "Month":
        df = calendar.by_month(fm, sel_cal)
    elif group_by == "Week":
        df = calendar.by_week(fm, sel_cal)
    elif group_by == "Activity":
        df = calendar.by_activity(sel_cal)
    else:
        logging.error(f"Key error: {group_by}")
        raise KeyError
    return df


def chart_all(df: pd.DataFrame, area_chart: bool):
    chart = alt.Chart(df).mark_area() if area_chart else alt.Chart(df).mark_bar()
    st.write(
        chart.properties(width=700, height=400).encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Sum of hours"),
            color=alt.Color(
                "Activity",
                scale=alt.Scale(
                    domain=[
                        "Chores",
                        "Commute",
                        "Eat",
                        "Entertainment",
                        "Personal care",
                        "Personal development",
                        "Spare time",
                        "Sport",
                        "Study",
                        "Work",
                    ],
                    range=[
                        "#7986CB",
                        "#9E69AF",
                        "#039BE5",
                        "#F4511E",
                        "#E67C73",
                        "#F6BF26",
                        "#B39DDB",
                        "#8E24AA",
                        "#33B679",
                        "#F09300",
                    ],
                ),
                legend=alt.Legend(title="Color Legend"),
            ),
        )
    )


def chart_single(df: pd.DataFrame, area_chart: bool):
    chart = alt.Chart(df).mark_area() if area_chart else alt.Chart(df).mark_bar()
    st.write(
        chart.properties(width=700, height=400).encode(
            x=alt.X("Period"),
            y=alt.Y("sum(Duration)", title="Hours"),
            color=alt.Color(
                "Activity",
                legend=alt.Legend(title="Color Legend"),
            ),
        )
    )


def decreasing_activity_chart(df: pd.DataFrame):
    st.write(
        alt.Chart(df.reset_index())
        .mark_bar(point=True)
        .encode(
            alt.X("Activity", sort="-y"),
            alt.Y("Duration", title="Hours"),
            color=alt.Color(
                "Activity",
                legend=alt.Legend(title="Color Legend"),
            ),
        )
        .properties(width=700, height=400)
    )


def normalize_to_one(df: pd.DataFrame, normalize: bool) -> pd.DataFrame:
    """Normalize data to 1 if required

    Args:
        df (pd.DataFrame): Input dataframe
        normalize (bool): If normalize

    Returns:
        pd.DataFrame: Output dataframe
    """
    if normalize:
        df_sum = df.groupby(["Period"]).sum().reset_index()
        df_sum.rename(columns={"Duration": "Duration_Month"}, inplace=True)
        df_new = pd.merge(df, df_sum, on="Period")
        df_new["Duration_Normalized"] = df_new["Duration"] / df_new["Duration_Month"]
        df["Duration"] = df_new["Duration_Normalized"]
    return df


def remove_last_month(df: pd.DataFrame) -> pd.DataFrame:
    """Remove last month of data from dataframe
    Set here and not in Calendar class so it's possible to filter data
    only in charts and not in table.

    Args:
        df (pd.DataFrame): input dataframe

    Returns:
        pd.DataFrame: output dataframe
    """
    month = datetime.datetime.today().strftime("%Y-%m")
    return df[df["Period"] < month]


def main():
    st.set_page_config(page_title="Calendar Analyzer", page_icon="⌛")
    st.title("Calendar Analyzer")
    st.caption(
        "[https://github.com/MarcoDiFrancesco/CalendarAnalyzer](https://github.com/MarcoDiFrancesco/CalendarAnalyzer)"
    )

    calendar = Calendar()
    group_by = show_group_by()
    fm = show_filter(calendar, group_by)

    # All activities
    st.markdown("---")
    st.header("All activities")
    df = get_df(calendar, group_by, fm)
    st.subheader("Chart 1")
    normalize, area_chart, _ = show_checkboxes(True, "1")
    df_norm = df.copy()
    df_norm = normalize_to_one(df_norm, normalize)
    df_norm = remove_last_month(df_norm)
    chart_all(df_norm, area_chart)
    table_sd_sum(df)

    # Selected activity
    st.markdown("---")
    st.header("Single activity")
    sel_cal = select_activity(calendar)
    df = get_df(calendar, group_by, fm, sel_cal)
    st.subheader("Chart 2")
    normalize, area_chart, _ = show_checkboxes(False, "2")
    df_norm = df.copy()
    df_norm = normalize_to_one(df_norm, normalize)
    df_norm = remove_last_month(df_norm)
    chart_single(df_norm, area_chart)
    df_by_activity = get_df(calendar, "Activity", fm, sel_cal)
    decreasing_activity_chart(df_by_activity)
    table_sd_sum(df)


if __name__ == "__main__":
    main()
