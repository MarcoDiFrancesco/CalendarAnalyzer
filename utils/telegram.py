import json
from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st


def user_plot():
    df = _data_by_user()
    df = df[df["messages_len"] > 100]
    chart = alt.Chart(df).mark_bar()
    st.write(
        chart.properties(width=700, height=400).encode(
            x=alt.X("name", title="User", sort="-y"),
            y=alt.Y("messages_len", title="Messages count"),
            # order=alt.Order("messages_len", sort="ascending"),
            # sort=alt.EncodingSortField(field="messages_len", order="ascending"),
        )
    )


def month_plot_user():
    df = _data_by_time()
    st.subheader("Messages distribution")
    st.write("Showing chats with at least 100 messages")
    df = df.groupby([df.period, df.name]).size().reset_index(name="size")
    df = df[df["size"] >= 100]
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=400)
        .encode(
            x=alt.X("period"),
            y=alt.Y("size", title="Users"),
            color=alt.Color(
                "name",
                legend=alt.Legend(title="Color Legend"),
            ),
        )
    )


def month_plot_sentreceived():
    df = _data_by_time()
    df = df.groupby([df.period, df.sent]).size().reset_index(name="size")
    st.write(
        alt.Chart(df)
        .mark_bar()
        .properties(width=700, height=400)
        .encode(
            x=alt.X("period"),
            y=alt.Y("size", title="Users"),
            color=alt.Color(
                "sent",
                legend=alt.Legend(title="Color Legend"),
            ),
        )
    )


def _from_json() -> list:
    p = Path() / "data" / "telegram" / "result.json"
    assert p.exists()
    with open(p, "r") as f:
        f_content = json.load(f)
    return f_content["chats"]["list"]


def _data_by_user() -> pd.DataFrame:
    """Get telgram dataframe
    Returns:
        pd.DataFrame:
                            name  messages_len
        0                    The         38165
        1              Alessando         37257
    """
    chats = _from_json()
    for idx in range(len(chats)):
        chats[idx]["messages_len"] = len(chats[idx]["messages"])
    df = pd.DataFrame(chats, columns=["name", "messages_len"])
    df = df.sort_values("messages_len", ascending=False)
    return df


def _data_by_time() -> pd.DataFrame:
    chats = _from_json()
    # msgs = []
    # for chat in chats:
    #     msgs += chat["messages"]
    # df = pd.DataFrame(chats)
    """
    FROM:
              name       type           id         messages
        0     Alessando  personal_chat  129693439  [{'id': 26773, 'type': 'message', 'date': '201...
    TO:
              id        type                 date                from  ...  name       sent
        0     26773  message  2018-09-26T15:26:50  Marco Di Francesco  ...  Alessando  Received
    """
    df = pd.json_normalize(
        chats, record_path=["messages"], meta=["name"], errors="ignore"
    )
    df["date"] = pd.to_datetime(df["date"])
    df.loc[df["from"] == "Marco Di Francesco", "sent"] = "Sent"
    df.loc[df["from"] != "Marco Di Francesco", "sent"] = "Received"
    df["period"] = df.date.dt.strftime("%Y-%m")
    return df
