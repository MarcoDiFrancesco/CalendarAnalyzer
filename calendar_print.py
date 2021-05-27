from Calendar import Calendar
import streamlit as st


def get_cal_type(calendars):
    """
    Show list of activities with duration:
    Algoritmi	45
    Reti	    44.5000
    Ingegneria 	39
    """
    radio = st.radio("Group by", options=["Month", "Week", "Activity"])
    if radio == "Month":
        calendar = calendars.by_month
    elif radio == "Week":
        calendar = calendars.by_week
    elif radio == "Activity":
        calendar = calendars.by_activity

    activities = ["Select value", *calendar]
    activity = st.selectbox("List of all the activities", activities)
    if activity == "Select value":
        return None
    return calendar[activity]


def list_all(df):
    st.table(df)


def chart_by_month(df):
    st.bar_chart(df)


def main():
    calendar = Calendar()
    st.title("Calendar Analyzer")
    df = get_cal_type(calendar)
    if df is None:
        return
    list_all(df)
    chart_by_month(df)


if __name__ == "__main__":
    main()
