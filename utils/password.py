import streamlit as st
import os
import pandas as pd


def get_password(df: pd.DataFrame) -> pd.DataFrame:
    """Return true if password is correct"""
    password = st.text_input("Enter a password", type="password")
    if os.environ.get("DEBUG"):
        return df
    if password == os.environ.get("PSW"):
        return df
    df = df[df.Calendar != "Work"]
    return df
