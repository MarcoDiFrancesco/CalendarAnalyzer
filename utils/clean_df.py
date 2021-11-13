import pandas as pd
import warnings


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = _to_datetime(df)
    df = _remove_first_month(df)
    df = _compute_duration(df)
    df = _remove_daily(df)
    df.loc[:, "SUMMARY"] = df.SUMMARY.apply(lambda x: x.strip())
    return df


def _to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    # Transforms dates in date format
    df["DTSTART"] = pd.to_datetime(df["DTSTART"])
    df["DTEND"] = pd.to_datetime(df["DTEND"])
    return df


def _remove_first_month(df: pd.DataFrame) -> pd.DataFrame:
    """Discard before date"""
    return df[df["DTSTART"] > "2019-12"]  # Real is 2019-11-16


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
