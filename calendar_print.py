from Calendar import Calendar
import streamlit as st
import pandas as pd
import altair as alt


def main():
    calendar = Calendar()
    st.title("Calendar Analyzer")
    password = st.text_input("Enter a password", type="password")
    PSW = "gigi"
    if password != PSW:
        return
    cal_type = st.radio("Group by", options=["Month", "Week", "Activity"])

    calendar_list = calendar.calendars["Calendar"].unique()
    calendar_list = ["Select value", *calendar_list]
    calendar_sel = st.selectbox("List of all calendars", calendar_list)
    if cal_type == "Month":
        df = calendar.by_month(calendar_sel, normalize=True)
    elif cal_type == "Week":
        df = calendar.by_week(calendar_sel, normalize=True)
    elif cal_type == "Activity":
        df = calendar.by_activity(calendar_sel)
    show_table = st.checkbox("Show table")

    if show_table:
        st.table(df)
    if cal_type == "Activity":
        alt_chart = (
            alt.Chart(df.reset_index())
            .mark_bar(point=True)
            .encode(
                alt.X("SUMMARY", title="Activity", sort="-y"),
                alt.Y("Duration", title="Hours"),
            )
            .properties(width=700, height=400)
        )
        st.write(alt_chart)
    else:
        st.bar_chart(df, height=400)


if __name__ == "__main__":
    main()
