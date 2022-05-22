import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import chart_calendar_vert, chart_decreasing_activity


def work(df: pd.DataFrame) -> None:
    df = df.copy()
    df = df[df["Calendar"] == "Work"]
    if not len(df.index):
        return
    st.header("Work")
    df = remove_last_month(df, "DTSTART")
    chart_calendar_vert(df, "Work")
    chart_decreasing_activity(df, "Work")
