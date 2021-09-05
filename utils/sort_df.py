import streamlit as st
from utils.table_sd_sum import get_dates


def sort_by_name(df, type_mw, base):
    goal, var = (80, 0.7) if type_mw == "M" else (18, 0.6)
    base_date, base_activity = get_dates(base)
    df.loc[
        df["Activity"].isin(base_activity) & ~df["Period"].isin(base_date),
        "Duration",
    ] = goal * var + df["Duration"] * (1 - var)
    return df
