import streamlit as st


def show_checkboxes(normalize):
    cb1, cb2, cb3 = st.columns(3)
    with cb1:
        res1 = st.checkbox(
            "Normalize",
            value=normalize,
            help="Normalize from 0 to 1 and sort values by Standard Deviation",
        )
    with cb2:
        res2 = st.checkbox("Area chart", value=normalize)
    with cb3:
        res3 = ""  # st.checkbox("TMP")
    return res1, res2, res3
