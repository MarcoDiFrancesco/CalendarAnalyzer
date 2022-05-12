import datetime
import warnings

import pandas as pd
import pytz
from dateutil.tz import tzlocal


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = _to_datetime(df)
    df = _set_timezone(df)
    df = _remove_first_month(df)
    df = _remove_future(df)
    df = _compute_duration(df)
    df = _remove_daily(df)
    df.loc[:, "SUMMARY"] = df.SUMMARY.apply(lambda x: x.strip())
    df = df.sort_values("DTSTART")
    return df


def _to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    # Transforms dates in date format
    df["DTSTART"] = pd.to_datetime(df["DTSTART"])
    df["DTEND"] = pd.to_datetime(df["DTEND"])
    return df


def _set_timezone(df: pd.DataFrame) -> pd.DataFrame:
    """ICS saves timezone in 2 variables for each calendar, not for each event.
    Each event is already shifted depending on the daylight saving, this means
    only 2 hours are added.
    """
    # Shift n hours ahead, e.g. 17:30:00 -> 19:30:00
    df["DTSTART"] = df["DTSTART"] + pd.DateOffset(hours=2)
    df["DTEND"] = df["DTEND"] + pd.DateOffset(hours=2)
    # Remove timezone, e.g. 19:30:00+02:00 -> 19:30:00
    df["DTSTART"] = df["DTSTART"].dt.tz_localize(None)
    df["DTEND"] = df["DTEND"].dt.tz_localize(None)
    return df


def _remove_first_month(df: pd.DataFrame) -> pd.DataFrame:
    """Discard before date"""
    return df[df["DTSTART"] > "2019-12"]  # Real is 2019-11-16


def _remove_future(df: pd.DataFrame) -> pd.DataFrame:
    """Remove events starting in the future"""
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    return df[df["DTSTART"] < tomorrow_str]


def _compute_duration(df: pd.DataFrame) -> pd.DataFrame:
    """Add Duration column in hour, e.g. 1.5"""
    with warnings.catch_warnings():
        # Solution to this warning not known
        warnings.simplefilter(
            action="ignore", category=pd.core.common.SettingWithCopyWarning
        )
        df.loc[:, "Duration"] = df.DTEND - df.DTSTART
        df.loc[:, "Duration"] = df["Duration"].dt.total_seconds() / 60 / 60
    return df


def _remove_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Remove daily/mulitple days activities and NaN"""
    return df[df.Duration > 0]
