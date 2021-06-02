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
import datetime
import numpy as np


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
        cals = []
        with open("calendars.json") as f:
            links = json.load(f)
            for link in links:
                cal = self.download_cal(link)
                cal = cal["VCALENDAR"][0]
                cal_name = cal["X-WR-CALNAME"]
                cal_content = pd.DataFrame(
                    data=cal["VEVENT"], columns=["SUMMARY", "DTSTART", "DTEND"]
                )
                cal_content["Calendar"] = cal_name
                cals.append(cal_content)
        return pd.concat(cals)

    def download_cal(self, link):
        """Download ics from Google Calendar, return json"""
        ics = requests.get(link).text
        with tempfile.NamedTemporaryFile(mode="w") as f:
            f.write(str(ics))
            json = jicson.fromFile(f.name)
        return json

    def edit_datetime(self):
        # Transforms dates in date format
        df = self.calendars
        df["DTSTART"] = pd.to_datetime(df["DTSTART"])
        df["DTEND"] = pd.to_datetime(df["DTEND"])

        # Discard before date
        df = df[df["DTSTART"] > "2019-11-16"]
        # Discard future events
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        df = df[df["DTSTART"] < today]

        # Calculates duration from start to end like:
        #     Groceries	0 days 01:00:00
        # Transform to minutes:
        #     Groceries	1
        df["Duration"] = df["DTEND"] - df["DTSTART"]
        df["Duration"] = df["Duration"].dt.total_seconds() / 60 / 60

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

        # Remove daily/mulitple days activities and NaN
        self.calendars = df[df.Duration > 0]

    def by_activity(self, calendar_sel):
        df = self.calendars
        if calendar_sel != "Select value":
            df = df.loc[df["Calendar"] == calendar_sel]
        df = df.sort_values(by=["Duration"], ascending=False)
        df = df.set_index(["Calendar", "SUMMARY"])
        df = df.sum(level=1)
        return df.sort_values(by=["Duration"], ascending=False)

    def by_month(self, calendar_sel, normalize=False):
        # 2021-03 FBK         3.00
        #         Update      1.00
        # 2021-04 FBK         2.0
        #         Update      4.00
        df = self.calendars
        return self.by_period(df, "M", calendar_sel, normalize)

    def by_week(self, calendar_sel, normalize=False):
        df = self.calendars
        return self.by_period(df, "W", calendar_sel, normalize)

    def get_active_days(self):
        df = self.calendars
        df["Days"] = df["DTSTART"].dt.to_period("D").astype("str")
        df["Months"] = df["DTSTART"].dt.to_period("M").astype("str")
        # df = df.groupby(["Days"])
        # df["DaysActive"] = df["DTSTART"].dt.to_period("D")

    def by_period(self, df, period, calendar_sel, normalize):
        if calendar_sel != "Select value":
            df = df.loc[df["Calendar"] == calendar_sel]

        # Hide warning: Converting to PeriodArray/Index representation will drop timezone information.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df["Period"] = df["DTSTART"].dt.to_period(period).astype("str")

        # 2020-11 Breakfast     31.00
        #         Dinner        33.00
        #         Lunch         26.50
        df = df.groupby(["Period", "SUMMARY"])
        df = df.sum()

        # 2020-11 Breakfast     31.00
        # 2020-11 Dinner        33.00
        # 2020-11 Lunch         26.50
        df = df.reset_index()

        # SUMMARY  Breakfast  Dinner  Lunch  Snack
        # Month
        # 2019-11      11.50   15.00   15.5    0.0
        # 2019-12      20.50   30.50   30.0    0.0
        # 2020-01      32.50   37.00   30.5    0.0
        df = df.pivot_table(index="Period", columns="SUMMARY", fill_value=0)["Duration"]

        # List of columns
        columns = list(df.columns.values)
        df = pd.DataFrame(df, columns=columns)
        return df
