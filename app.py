from Calendar import Calendar
import streamlit as st
import pandas as pd
import altair as alt


def main():
    calendar = Calendar()
    st.title("Calendar Analyzer")
    password = st.text_input("Enter a password", type="password")
    PSW = "gigi"
    if password != PSW:
        return
    # Make radio horizontal
    st.write(
        "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
        unsafe_allow_html=True,
    )
    cal_type = st.radio("Group by", options=["Month", "Week", "Activity"])

    calendar_list = calendar.calendars["Calendar"].unique()
    calendar_list = ["Select value", *calendar_list]
    calendar_sel = st.selectbox("List of all calendars", calendar_list)
    if cal_type == "Month":
        df = calendar.by_month(calendar_sel, normalize=True)
    elif cal_type == "Week":
        df = calendar.by_week(calendar_sel, normalize=True)
    elif cal_type == "Activity":
        df = calendar.by_activity(calendar_sel)

    show_table = st.checkbox("Show data")
    if show_table:
        st.table(df)

    # Sort data
    if not cal_type == "Activity":
        normalize_by_default = calendar_sel == "Select value"
        df = sort_df(df, normalize_by_default)

    if cal_type == "Activity":
        alt_chart = (
            alt.Chart(df.reset_index())
            .mark_bar(point=True)
            .encode(
                alt.X("SUMMARY", title="Activity", sort="-y"),
                alt.Y("Duration", title="Hours"),
            )
            .properties(width=700, height=400)
        )
        st.write(alt_chart)
    else:
        st.bar_chart(df, height=350)
        st.area_chart(df, height=350)


def sort_df(df, normalize_by_default):
    if normalize_by_default:
        options = ["Standard deviation", "Sum", "Nope"]
    else:
        options = ["Nope", "Standard deviation", "Sum"]
    normalize_by = st.radio("Normalize by", options=options)
    if normalize_by == "Nope":
        return df
    if normalize_by == "Sum":
        sorted_df = df.sum().sort_values()
    elif normalize_by == "Standard deviation":
        sorted_df = df.std().sort_values()

    # Show table with std or sum
    st.dataframe(sorted_df.sort_values(ascending=False).astype(int))

    # Normalize by sum
    df = df.div(df.sum(axis=1), axis=0)

    # Sort one up, one down
    new_sort = []
    for element in sorted_df.index:
        new_sort.insert(len(new_sort) // 2, element)

    # Reverse order, in this case looks better
    new_sort = new_sort[::-1]

    # Reorder columns
    df = df[new_sort]

    # Add number because chart orders by name
    for i, row in enumerate(df):
        df.rename(columns={row: f"{i}-{row}"}, inplace=True)
    return df


# def sort_by_sum(df):
#     sorted_df = df.sum().sort_values()
#     st.dataframe(sorted_df)
#     # Normalize by sum
#     df = df.div(df.sum(axis=1), axis=0)
#     df = df[sorted_df.index]
#     return df


# def sort_by_std(df):
#     sorted_df = df.std().sort_values()
#     st.dataframe(sorted_df)


if __name__ == "__main__":
    main()
