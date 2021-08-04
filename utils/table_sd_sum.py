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


def get_dates(base=True):
    print("BASE", base)
    if not base:
        return [], []
    base_date = [
        "2019-12",
        "2019-12-02/2019-12-08",
        "2019-12-09/2019-12-15",
        "2020-09",
        "2020-08-31/2020-09-06",
        "2020-09-07/2020-09-13",
        "2020-09-14/2020-09-20",
        "2020-09-28/2020-10-04",
        "2021-09",
    ]
    base_activity = ["Work", "FBK"]
    return base_date, base_activity
