import streamlit as st
from utils.table_sd_sum import get_dates


def sort_df(df, normalize):
    if not normalize:
        return df

    # Normalize by sum
    # sorted_df = df.sum().sort_values()
    # Normalize by standard deviation
    sorted_df = df.std().sort_values()

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


def sort_by_name(df, type_mw, base):
    goal, var = (80, 0.7) if type_mw == "M" else (18, 0.6)
    base_date, base_activity = get_dates(base)
    df.loc[
        df["Activity"].isin(base_activity) & ~df["Period"].isin(base_date),
        "Duration",
    ] = goal * var + df["Duration"] * (1 - var)
    return df
