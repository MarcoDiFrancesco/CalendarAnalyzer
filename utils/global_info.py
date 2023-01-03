import pandas as pd
import streamlit as st


def global_info(df: pd.DataFrame) -> None:
    days = len(df["DAY"].unique())
    n_act = len(df)
    st.markdown(
        # Trailing spaces removed by pre-commit
        f"""
        🟢 Beginning date: Jan 2020 - Dec 2022 (3 years)

        ⌛ Elapsed days: {days}

        🧮 Total activities: {n_act} (~{n_act/days:.0f} per day)
        """
    )
