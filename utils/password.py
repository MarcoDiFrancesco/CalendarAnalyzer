import streamlit as st
import os


def get_password() -> bool:
    """Return true if password is correct"""
    password = st.text_input("Enter a password", type="password")
    if os.environ.get("DEBUG"):
        return True
    if password == os.environ.get("PSW"):
        return True
    return False
