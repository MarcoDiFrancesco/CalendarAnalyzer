import pandas as pd
import streamlit as st


def global_info(df: pd.DataFrame) -> None:
    days = len(df["DAY"].unique())
    n_act = len(df)
    st.markdown(
        # Trailing spaces removed by pre-commit
        f"""
        🟢 Beginning date: Dec 2019

        ⌛ Elapsed days: {days}

        🧮 Total activities: {n_act}
        """
    )
