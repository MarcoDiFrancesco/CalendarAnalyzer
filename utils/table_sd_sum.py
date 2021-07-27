import pandas as pd
import streamlit as st


def table_sd_sum(df: pd.DataFrame) -> pd.DataFrame:
    st.subheader("Data table")
    df_sum = df.sum().astype(int)
    df_std = df.std().astype(int)

    df = pd.concat([df_sum, df_std], axis=1)
    df.columns = ["Sum", "SD"]
    df.sort_values(by="Sum", ascending=False, inplace=True)
    return df
