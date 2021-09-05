import streamlit as st
import uuid
from typing import Tuple


def show_checkboxes(
    default: bool,
    key: str,
) -> Tuple[bool, bool, bool]:
    """Show 3 buttons: Normalize, Area chart, EMPTY

    Args:
        default (bool): Selected by default

    Returns:
        (bool, bool, bool): True if checkbox selected
    """
    cb1, cb2, cb3 = st.columns(3)
    with cb1:
        res1 = st.checkbox(
            "Normalize",
            value=default,
            help="Normalize from 0 to 1 and sort values by Standard Deviation",
            key=f"cb1-{key}",
        )
    with cb2:
        res2 = st.checkbox(
            "Area chart",
            help="Show Area chart instead of Bar chart",
            key=f"cb2-{key}",
        )
    with cb3:
        res3 = False  # st.checkbox("TMP")
    return res1, res2, res3
