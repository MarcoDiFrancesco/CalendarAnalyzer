import concurrent.futures
import copy
import datetime
import json
import os
import tempfile
import warnings

import jicson
import pandas as pd
import requests
import streamlit as st

persist = True if not os.environ.get("DEBUG") else False


# Cache for 1 week
@st.cache(ttl=7 * 24 * 60 * 60, persist=persist)
def download_cals() -> pd.DataFrame:
    """Download calendars."""
    cals = []
    links = os.getenv("CALENDAR_LINKS")
    assert (
        links
    ), "Environment variable CALENDAR_LINKS not found, did you source .envvar?"

    links = json.loads(links)
    # Check added for linter
    assert links is not None
    # Parallelize calendars download
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_link_map = {executor.submit(_download_cal, link): link for link in links}
        for future in concurrent.futures.as_completed(future_link_map):
            link = future_link_map[future]
            cal = future.result()
            cal = cal["VCALENDAR"][0]
            cal_name = cal["X-WR-CALNAME"]
            cal_content = pd.DataFrame(
                data=cal["VEVENT"], columns=["SUMMARY", "DTSTART", "DTEND", "UID"]
            )
            cal_content["Calendar"] = cal_name
            cal_content["CAL_LINK"] = link
            cals.append(cal_content)
    return pd.concat(cals)


def _download_cal(link: str):
    """Download ics from Google Calendar, return json."""
    if link.startswith("http"):
        ics = requests.get(link, timeout=5).text
    else:
        with open(link, "r") as f:
            ics = f.read()
    # Convert ics to json
    cal = jicson.fromText(ics)
    return cal
