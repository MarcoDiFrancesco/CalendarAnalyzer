from Calendar import Calendar
import streamlit as st
import pandas as pd


def get_cal_type(calendars):
    """
    Show list of activities with duration:
    Algoritmi	45
    Reti	    44.5000
    Ingegneria 	39
    """
    cal_type = st.radio("Group by", options=["Month", "Week", "Activity"])
    if cal_type == "Month":
        calendar = calendars.by_month
    elif cal_type == "Week":
        calendar = calendars.by_week

    activities = ["Select value", *calendar]
    activity = st.selectbox("List of all the activities", activities)
    if activity == "Select value":
        return None
    return cal_type, calendar[activity]


def list_all(df):
    st.table(df)


def chart_by_activity(df):
    st.bar_chart(df)


def stacked_chart(df):
    # List of columns
    columns = list(df.columns.values)
    df = pd.DataFrame(df, columns=columns)
    st.bar_chart(df)


def main():
    calendar = Calendar()
    st.title("Calendar Analyzer")
    cal_type, df = get_cal_type(calendar)
    if df is None:
        return
    if cal_type == "Month":
        # df = calendar.by_month
        stacked_chart(df)
    elif cal_type == "Week":
        pass
    elif cal_type == "Activity":
        df = calendar.by_activity
        list_all(df)
        chart_by_activity(df)


if __name__ == "__main__":
    main()
