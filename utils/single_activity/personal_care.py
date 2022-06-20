import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import chart_calendar_vert, chart_decreasing_activity


def personal_care(df: pd.DataFrame) -> None:
    """Removed category due to luck of data meaning.

    Details: https://github.com/MarcoDiFrancesco/CalendarAnalyzer/issues/94
    """
    df = df.copy()
    st.header("Personal care")
    df = remove_last_month(df, "DTSTART")
    chart_calendar_vert(df, "Personal care")
    chart_decreasing_activity(df, "Personal care")
