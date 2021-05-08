import pandas as pd
import streamlit as st

import json
import requests
import jicson
import os
import uuid


def _get_cal(cal_link):
    """
    Download ics from Google Calendar, write it to a temp file and return data in json form
    """
    ics = requests.get(cal_link).text
    file_path = f"/tmp/{uuid.uuid4()}-calendar.ics"
    with open(file_path, "w") as f:
        f.write(str(ics))
    json = jicson.fromFile(file_path)
    os.remove(file_path)
    return json


# @st.cache(allow_output_mutation=True)
def get_calendars():
    """Get dictionary of calendars"""

    calendars = {}
    with open("calendars.json") as f:
        cal_links = json.load(f)
        for cal_link in cal_links:
            cal = _get_cal(cal_link)
            cal = cal["VCALENDAR"][0]
            cal_name = cal["X-WR-CALNAME"]
            cal_content = cal["VEVENT"]
            cal_content = pd.DataFrame(
                data=cal_content, columns=["SUMMARY", "DTSTART", "DTEND"]
            )
            calendars[cal_name] = cal_content
    return calendars


def cal_to_datetime(calendars):
    """Make dates in python date library format"""
    for name, events in calendars.items():
        events["DTSTART"] = pd.to_datetime(events["DTSTART"])
        events["DTEND"] = pd.to_datetime(events["DTEND"])
    return calendars


def get_duration(calendars):
    """
    Calculates duration from start to end like:
    Groceries	0 days 01:00:00
    Transform to minutes:
    Groceries	1
    """
    for name, events in calendars.items():
        events["Duration"] = events["DTEND"] - events["DTSTART"]
        events["Duration"] = events["Duration"].dt.total_seconds() / 60 / 60
    return calendars


def set_index(calendars):
    """
    From :
    1	Groceries	0 days 01:00:00
    2	Shopping	0 days 01:00:00
    3	Groceries	0 days 01:00:00
    With index:
    Groceries	0 days 01:00:00
    Shopping	0 days 01:00:00
    Groceries	0 days 01:00:00
    Sum:
    Groceries	0 days 02:00:00
    Shopping	0 days 01:00:00
    """
    for name, events in calendars.items():
        events = events.set_index("SUMMARY")
        events = events.sum(level=0)
        calendars[name] = events
    return calendars


if __name__ == "__main__":
    calendars = get_calendars()
    calendars = cal_to_datetime(calendars)
    calendars = get_duration(calendars)
    calendars = set_index(calendars)
    st.title("Calendar data")
    for name, calendar in calendars.items():
        st.line_chart(calendar)

    # # Add value column with minutes
    # hour = df["DTSTART"].dt.hour
    # minute = df["DTSTART"].dt.minute
    # minute = hour * 60 + minute
    # df["value"] = minute

    # df.set_index("DTSTART")
    # return df

    # df = create_data_frame(cal)
    # # print(df)
    # #

    # options = list(dict.fromkeys(df["SUMMARY"]))
    # option = st.selectbox("Which activity you'd like to visualize?", options)
