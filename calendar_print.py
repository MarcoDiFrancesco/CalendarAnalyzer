from Calendar import Calendar
import streamlit as st
import pandas as pd


def main():
    calendar = Calendar()
    st.title("Calendar Analyzer")
    cal_type = st.radio("Group by", options=["Month", "Week", "Activity"])

    activities = ["Select value", *calendar.calendars]
    activity = st.selectbox("List of all the activities", activities)
    if activity == "Select value":
        return
    if cal_type == "Month":
        df = calendar.by_month
    elif cal_type == "Week":
        df = calendar.by_week
    elif cal_type == "Activity":
        df = calendar.by_activity
    df = df[activity]

    if cal_type == "Activity":
        st.table(df)
    st.bar_chart(df, height=400)


if __name__ == "__main__":
    main()
