import datetime

import pandas as pd
import streamlit as st
from streamlit.elements.arrow import Data

from . import cal_link, check_day, check_minute, check_name
from .error_table import show_error_table


def data_checks(df: pd.DataFrame):
    """Show list of all the activities that are broken."""
    df = df.copy()
    # Remove today's activities
    df = df[df["DTSTART"] < datetime.date.today().strftime("%Y-%m-%d")]
    df = _compute_errors(df)
    show_error_table(df)


@st.cache
def _compute_errors(df: pd.DataFrame):
    """Compute errors and cache them."""
    cal_link.get_cal_link(df)
    # check_minute.check_minute(df)
    # check_day.check_day(df)
    check_name.check_name(df)
    # Cache must return an object
    return df
