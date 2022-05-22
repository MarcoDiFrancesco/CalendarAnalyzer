import pandas as pd
import streamlit as st

from utils.remove_last_month import remove_last_month
from utils.single_activity import chart_calendar_vert, chart_decreasing_activity


def commute(df: pd.DataFrame) -> None:
    df = df.copy()
    st.header("Commute")
    df = remove_last_month(df, "DTSTART")
    chart_calendar_vert(df, "Commute")
    chart_decreasing_activity(df, "Commute")
