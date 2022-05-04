import base64
from urllib import parse

import pandas as pd


def get_cal_link(df: pd.DataFrame):
    """Compute calendar link described in:
    https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/58

    Columns taken into consideration:
    - UID: https://calendar.google.com/.../basic.ics
    - CAL_LINK: xxxxxxxxx@google.com
    """
    # From: 64xxxxxxxco@google.com
    # To:   64xxxxxxxco
    df["UID"] = df["UID"].str.split("@", expand=True)[0]
    # From: https://calendar.google.com/calendar/ical/t2xxxxxxxxxxxxxxxxxxxxx64%40group.calendar.google.com/private-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/basic.ics
    # To:   t2xxxxxxxxxxxxxxxxxxxxx64%40group.calendar.google.com
    df["CAL_LINK"] = df["CAL_LINK"].str.split("/", expand=True)[5]
    # %40 to @
    df["CAL_LINK"] = df["CAL_LINK"].apply(parse.unquote)
    # From: t2xxxxxxxxxxxxxxxxxxxxxx64@group.calendar.google.com
    # To:   t2xxxxxxxxxxxxxxxxxxxxxx64@g
    df["CAL_LINK"] = df["CAL_LINK"].str.split("@", expand=True)[0] + "@g"
    df["EVENT_LINK"] = df["UID"] + " " + df["CAL_LINK"]
    # String to bytes
    df["EVENT_LINK"] = df["EVENT_LINK"].str.encode("utf-8", "strict")
    # Bytes to base64
    df["EVENT_LINK"] = df["EVENT_LINK"].apply(base64.b64encode)
    # Bytes to string
    df["EVENT_LINK"] = df["EVENT_LINK"].str.decode("utf-8")
    df["EVENT_LINK"] = (
        "https://calendar.google.com/calendar/u/0/r/eventedit/" + df["EVENT_LINK"]
    )
    # return df
