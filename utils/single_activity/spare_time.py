import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import chart_calendar_vert, chart_decreasing_activity


def spare_time(df: pd.DataFrame) -> None:
    df = df.copy()
    df = df[df["Calendar"] == "Spare time"]
    st.header("Spare time")
    df = remove_last_month(df, "DTSTART")
    chart_calendar_vert(df, "Spare time")
    chart_decreasing_activity(df, "Spare time")