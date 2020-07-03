import json
import os
import uuid

import jicson
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import streamlit as st

st.title("Calendar data")


@st.cache(allow_output_mutation=True)
def get_data(link):
    """
    Download ics from Google Calendar, write it to a temp file
    and return data in json form
    """
    ics = requests.get(link).text
    file_path = f"/tmp/{uuid.uuid4()}-calendar.ics"
    with open(file_path, "w") as f:
        f.write(str(ics))
    json = jicson.fromFile(file_path)
    os.remove(file_path)
    return json["VCALENDAR"][0]["VEVENT"]


def date_edit(data):
    """
    Make dates in python date library format
    """

    for d in data:
        try:
            for col_name in ["DTSTART", "DTEND", "DTSTAMP", "CREATED", "LAST-MODIFIED"]:
                d[col_name] = pd.to_datetime(d[col_name])
        except KeyError as e:
            print(e)
    return data


def create_data_frame(data):
    df = pd.DataFrame(data, columns=["DTSTART", "DTEND", "SUMMARY"])

    # Add duration of the events column
    df["Duration"] = df["DTEND"] - df["DTSTART"]

    # Filter only breakfast
    # df = df[df["SUMMARY"] == "Breakfast"]

    # Add value column with minutes
    hour = df["DTSTART"].dt.hour
    minute = df["DTSTART"].dt.minute
    minute = hour * 60 + minute
    df["value"] = minute

    df.set_index("DTSTART")
    return df


with open("calendars.json") as data_file:
    data = json.load(data_file)
    for calendars in data:
        data = get_data(calendars["CAL_LINK"])
        data = date_edit(data)
        df = create_data_frame(data)
        print(df)
        st.line_chart(df)

        options = list(dict.fromkeys(df["SUMMARY"]))
        option = st.selectbox("Which activity you'd like to visualize?", options)
