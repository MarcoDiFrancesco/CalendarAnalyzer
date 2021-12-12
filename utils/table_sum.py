import pandas as pd
import streamlit as st
import numpy as np


def table_sum(df: pd.DataFrame, calendar: str = None):
    """Table with sum and standar deviation for each activity

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Output DataFrame
    """
    st.markdown(
        "**Standard Deviation** is computed on all activities over the sum of them"
    )
    if calendar is not None:
        df = df[df.Calendar == calendar]
        index = "SUMMARY"
    else:
        index = "Calendar"
    df = df.filter([index, "Duration"])
    df_sum = df.groupby(index).sum()
    df_std = df.groupby(index).std() / df_sum * 1000
    # Set NaN to 0
    df_std["Duration"] = df_std["Duration"].fillna(0)
    # Float to int
    df_sum = df_sum.astype("int")
    df_std = df_std.astype("int")
    df = pd.concat([df_sum, df_std], axis=1)
    df.columns = ["Sum", "SD"]
    df.sort_values(by="Sum", ascending=False, inplace=True)
    st.write(df)
