import altair as alt
import pandas as pd
import streamlit as st

from utils.group_by_period import group_by_period
from utils.remove_last_month import remove_last_month


def single_activity_text(df: pd.DataFrame) -> None:
    act_tot = len(df.index)
    st.markdown(
        """
        ---
        # Single activity
        """
    )


def filter_df_chart(df: pd.DataFrame, calendar: str) -> pd.DataFrame:
    df = group_by_period(df, "M")
    df = df.groupby(["Period", "Calendar", "SUMMARY"]).sum().reset_index()
    df = df.loc[df["Calendar"] == calendar]
    return df


def fill_missing_months(
    df: pd.DataFrame, col_month: str, cat_month: str
) -> pd.DataFrame:
    """Fill missing months in some categories."""
    df = pd.pivot_table(
        df,
        values="Duration",
        index="SUMMARY",
        columns="Period",
        fill_value=0,
        aggfunc="sum",
    )
    df = df.reset_index()
    df = df.melt(id_vars="SUMMARY", var_name="Period", value_name="Duration")
    return df
