import pandas as pd
import streamlit as st
import numpy as np


def table_sd_sum(df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Table")
    st.markdown(
        "**Standard Deviation** is calculated on all activities over the sum of them"
    )
    df_sum = df.sum().astype(int)
    df_std = df.std() / df_sum * 1000
    df = df.replace(np.inf, 1)
    df = df.fillna(0)

    # df_std = df_std.astype(int)

    df = pd.concat([df_sum, df_std], axis=1)
    df.columns = ["Sum", "SD"]
    df.sort_values(by="Sum", ascending=False, inplace=True)
    return df
