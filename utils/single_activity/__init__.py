import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.remove_last_month import remove_last_month


def single_activity_text(df: pd.DataFrame):
    act_tot = len(df.index)
    st.markdown(
        f"""
        ---
        # Single activity
        """
    )


def filter_df_chart(df: pd.DataFrame, calendar: str):
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = df.loc[df["Calendar"] == calendar]
    return df
