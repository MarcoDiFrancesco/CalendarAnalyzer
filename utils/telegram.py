import json
from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st


def telegram_data() -> pd.DataFrame:
    p = Path() / "data" / "telegram" / "result.json"
    assert p.exists()
    with open(p, "r") as f:
        f_content = json.load(f)
    chats = f_content["chats"]["list"]
    for idx in range(len(chats)):
        chats[idx]["messages_len"] = len(chats[idx]["messages"])
    df = pd.DataFrame(chats, columns=["name", "messages_len"])
    df = df.sort_values("messages_len", ascending=False)
    return df


def telegram_plot(df: pd.DataFrame):
    chart = alt.Chart(df).mark_bar()
    print("GIGI", df)
    st.write(
        chart.properties(width=700, height=400).encode(
            x=alt.X("name", title="User", sort="-y"),
            y=alt.Y("messages_len", title="Messages count"),
            # order=alt.Order("messages_len", sort="ascending"),
            # sort=alt.EncodingSortField(field="messages_len", order="ascending"),
        )
    )
