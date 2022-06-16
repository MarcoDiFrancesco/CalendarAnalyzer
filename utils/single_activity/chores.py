import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import chart_calendar_vert, chart_decreasing_activity


def chores(df: pd.DataFrame) -> None:
    df = df.copy()
    st.header("Chores")
    st.markdown(
        """
        Observations:
        - Spike beginning of 2022: I chose the university and organized courses
        """
    )
    df = remove_last_month(df, "DTSTART")
    chart_calendar_vert(df, "Chores")
    chart_decreasing_activity(df, "Chores")
