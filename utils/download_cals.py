import json
import requests
import jicson
import streamlit as st
import pandas as pd
import tempfile
import copy
import warnings
import datetime
import os

# from utils.sort_df import sort_by_name

# Cache for 1 week
@st.cache(ttl=7 * 24 * 60 * 60)
def download_cals() -> pd.DataFrame:
    """Download calendars"""
    cals = []
    links = os.getenv("CALENDAR_LINKS")
    assert (
        links
    ), "Environment variable CALENDAR_LINKS not found, did you source .envvar?"
    links = json.loads(links)
    for link in links:
        cal = _download_cal(link)
        cal = cal["VCALENDAR"][0]
        cal_name = cal["X-WR-CALNAME"]
        cal_content = pd.DataFrame(
            data=cal["VEVENT"], columns=["SUMMARY", "DTSTART", "DTEND"]
        )
        cal_content["Calendar"] = cal_name
        cals.append(cal_content)
    return pd.concat(cals)


def _download_cal(link: str):
    """Download ics from Google Calendar, return json"""
    ics = requests.get(link).text
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write(str(ics))
        json = jicson.fromFile(f.name)
    return json
