import json
import requests
import jicson
import os
import uuid
import streamlit as st
import pandas as pd


def _get_from_link(cal_link):
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


@st.cache(allow_output_mutation=True)
def get_google_calendars():
    calendars = {}
    with open("calendars.json") as f:
        cal_links = json.load(f)
        for cal_link in cal_links:
            cal = _get_from_link(cal_link)
            cal = cal["VCALENDAR"][0]
            cal_name = cal["X-WR-CALNAME"]
            cal_content = cal["VEVENT"]
            cal_content = pd.DataFrame(
                data=cal_content, columns=["SUMMARY", "DTSTART", "DTEND"]
            )
            calendars[cal_name] = cal_content
    return calendars
