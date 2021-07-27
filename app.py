import os
from Calendar import Calendar
import streamlit as st
import altair as alt
import sentry_sdk
from utils.sort_df import sort_df
import logging
from utils.table_sd_sum import table_sd_sum
from utils.show_checkboxes import show_checkboxes


def show_table(group_by, df):
    if group_by == "Month" or group_by == "Week":
        st.write(table_sd_sum(df))
    else:
        st.write(df)


def show_bar_chart(group_by, df, sel_cal):
    st.subheader("Bar chart")
    if group_by == "Month" or group_by == "Week":
        normalize = sel_cal == "Select value"
        normalize, area_chart, _ = show_checkboxes(normalize)
        df = sort_df(df, normalize)
        if area_chart:
            st.area_chart(df, height=350)
        else:
            st.bar_chart(df, height=350)
    else:
        st.write(
            alt.Chart(df.reset_index())
            .mark_bar(point=True)
            .encode(
                alt.X("SUMMARY", title="Activity", sort="-y"),
                alt.Y("Duration", title="Hours"),
            )
            .properties(width=700, height=400)
        )


def show_filter(calendar):
    # Show radio options horizontally
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )

    # Group by type
    group_by = st.radio("Group by", options=["Month", "Week", "Activity"])
    cal_list = calendar.calendars["Calendar"].unique()
    cal_list = ["Select value", *cal_list]
    sel_cal = st.selectbox("List of all calendars", cal_list)

    # Filter section
    filter = st.beta_expander("Filters")
    with filter:
        st.write("TO IMPLEMENT")
        start, stop = st.select_slider(
            "Restrict period",
            ["01/20", "02/20", "03/20"],
            value=("01/20", "02/20"),
        )
    if group_by == "Month":
        df = calendar.by_month(sel_cal, normalize=True)
    elif group_by == "Week":
        df = calendar.by_week(sel_cal, normalize=True)
    elif group_by == "Activity":
        df = calendar.by_activity(sel_cal)
    else:
        logging.error(f"Key error: {group_by}")
        raise KeyError

    return group_by, df, sel_cal


def main():
    calendar = Calendar()
    st.title("Calendar Analyzer")

    # Require password
    password = st.text_input("Enter a password", type="password")
    PSW = "gigi"
    if password != PSW:
        return

    group_by, df, sel_cal = show_filter(calendar)
    show_table(group_by, df)
    show_bar_chart(group_by, df, sel_cal)


def sentry():
    key = os.environ.get("SENTRY_KEY")
    if key:
        sentry_sdk.init(key, traces_sample_rate=1.0)


if __name__ == "__main__":
    sentry()
    main()
