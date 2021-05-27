import json
from numpy import NaN
from pandas._libs.tslibs import NaT
import requests
import jicson
import streamlit as st
import pandas as pd
import tempfile
import copy
import warnings


class Calendar:
    """Google calendar class"""

    def __init__(self):
        # Dictionary containing calendars
        cached_calendars = self.download_cals()
        # copy.copy throws warning
        self.calendars = copy.deepcopy(cached_calendars)
        self.edit_datetime()

    @st.cache
    def download_cals(self):
        """Download calendars"""
        calendars = {}
        with open("calendars.json") as f:
            links = json.load(f)
            for link in links:
                cal = self.download_cal(link)
                cal = cal["VCALENDAR"][0]
                cal_name = cal["X-WR-CALNAME"]
                cal_content = pd.DataFrame(
                    data=cal["VEVENT"], columns=["SUMMARY", "DTSTART", "DTEND"]
                )
                calendars[cal_name] = cal_content
        return calendars

    def download_cal(self, link):
        """Download ics from Google Calendar, return json"""
        ics = requests.get(link).text
        # file_path = f"/tmp/{uuid.uuid4()}-calendar.ics"
        # with open(file_path, "w") as f:
        #     f.write(str(ics))
        with tempfile.NamedTemporaryFile(mode="w") as f:
            f.write(str(ics))
            json = jicson.fromFile(f.name)
        return json

    def edit_datetime(self):
        for name, df in self.calendars.items():
            # Transforms dates in date format
            df["DTSTART"] = pd.to_datetime(df["DTSTART"])
            df["DTEND"] = pd.to_datetime(df["DTEND"])

            # Calculates duration from start to end like:
            #     Groceries	0 days 01:00:00
            # Transform to minutes:
            #     Groceries	1
            df["Duration"] = df["DTEND"] - df["DTSTART"]
            df["Duration"] = df["Duration"].dt.total_seconds() / 60 / 60

            # From: 'Dinner with Pietro'
            # Summary: 'Dinner'
            # Descrip: 'with Pietro'
            df["SUMMARY"] = df["SUMMARY"].str.split(" ").str[0]
            df["Description"] = df["SUMMARY"].str.split(" ")[1:].str.join(" ")

            # Add index
            # From:
            #     1	Groceries	0 days 01:00:00
            #     2	Shopping	0 days 01:00:00
            #     3	Groceries	0 days 01:00:00
            # With index:
            #     Groceries	0 days 01:00:00
            #     Shopping	0 days 01:00:00
            #     Groceries	0 days 01:00:00
            # df = df.set_index("SUMMARY")

            # Sort
            df = df.sort_values(by=["Duration", "SUMMARY"], ascending=False)

            # Remove daily/mulitple days activities and NaN
            self.calendars[name] = df[df.Duration > 0]

    @property
    def by_activity(self):
        # Sum:
        #     Groceries	0 days 02:00:00
        #     Shopping	0 days 01:00:00
        calendars = {}
        for name, df in self.calendars.items():
            df = df.set_index(["SUMMARY"])
            df = df.sum(level=0)
            calendars[name] = df
        return calendars

    @property
    def by_month(self):
        # 2021-03 FBK         3.00
        #         Update      1.00
        # 2021-04 FBK         2.0
        #         Update      4.00
        calendars = {}
        for name, df in self.calendars.items():
            # Hide warning: Converting to PeriodArray/Index representation will drop timezone information.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df["Month"] = df["DTSTART"].dt.to_period("M").astype("str")
            # df.set_index(["Month", "SUMMARY"])
            df = df.groupby(["Month", "SUMMARY"])
            df = df.sum()
            calendars[name] = df
        return calendars

    @property
    def by_week(self):
        calendars = {}
        for name, df in self.calendars.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df["Week"] = df["DTSTART"].dt.to_period("W").astype("str")
            # df = df.set_index(["Week", "SUMMARY"])
            df = df.groupby(["Week", "SUMMARY"])
            df = df.sum()
            calendars[name] = df
        return calendars
