import os
from utils.Calendar import Calendar
import streamlit as st
import altair as alt
from utils.sort_df import sort_df
import logging
from utils.table_sd_sum import table_sd_sum
from utils.show_checkboxes import show_checkboxes


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
    return st.radio("Group by", options=["Month", "Week", "Activity"])


def select_activity(calendar):
    cal_list = calendar.calendars["Calendar"].unique()
    return st.selectbox("List of all calendars", cal_list)


def show_filter(calendar, group_by):
    # Filter section
    filter = st.beta_expander("Filters")
    with filter:
        st.write("TO IMPLEMENT")
        if not get_password():
            return True
        start, stop = st.select_slider(
            "Restrict period",
            ["01/20", "02/20", "03/20"],
            value=("01/20", "02/20"),
        )


def get_df(calendar, group_by, fm, sel_cal=None):
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


def show_table(group_by, df):
    if group_by == "Month" or group_by == "Week":
        st.write(table_sd_sum(df))
    else:
        st.write(df)


def show_bar_chart(group_by, df, sel_cal=None):
    st.subheader("Chart")
    if group_by == "Month" or group_by == "Week":
        normalize = sel_cal is None
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


def main():
    st.set_page_config(page_title="Calendar Analyzer", page_icon="⌛")
    st.title("Calendar Analyzer")

    calendar = Calendar()
    group_by = show_group_by()
    fm = show_filter(calendar, group_by)

    # All activities
    st.markdown("---")
    st.header("All activities")
    df = get_df(calendar, group_by, fm)
    show_bar_chart(group_by, df)
    show_table(group_by, df)

    # Selected activity
    st.markdown("---")
    st.header("Single activity")
    sel_cal = select_activity(calendar)
    df = get_df(calendar, group_by, fm, sel_cal)
    show_bar_chart(group_by, df, sel_cal)
    show_table(group_by, df)


if __name__ == "__main__":
    main()
