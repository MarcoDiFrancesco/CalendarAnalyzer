import datetime
import os

import pandas as pd
import streamlit as st
from streamlit.elements.arrow import Data

from . import cal_link, check_day, check_minute, check_name

# from .error_table import show_error_table
from .error_table import table_errors


def data_checks(df: pd.DataFrame):
    """Show list of all the activities that are broken."""
    df = df.copy()
    # Remove today's activities
    df = df[df["DTSTART"] < datetime.date.today().strftime("%Y-%m-%d")]
    with st.expander("Errors list"):
        if st.button("Compute errors"):
            df = _compute_errors(df)
            # Remove rows without errors
            df = df[~df["Error"].isna()]
            st.write(f"Total errors: {len(df)}")
            # Take at most n elements
            df = df[: min(len(df), 30)]
            table_errors(df)

    # show_error_table(df)


# @st.cache(ttl=7 * 24 * 60 * 60)
@st.experimental_memo
def _compute_errors(df: pd.DataFrame):
    """Compute errors and cache them."""
    cal_link.get_cal_link(df)
    check_minute.check_minute(df)
    check_day.check_day(df)
    check_name.check_name(df)
    # Cache must return an object
    return df
