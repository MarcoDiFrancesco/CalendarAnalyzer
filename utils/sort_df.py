import streamlit as st


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
