import pandas as pd
import streamlit as st


def table_sum(df: pd.DataFrame, calendar: str | None = None):
    """Table with sum and standar deviation for each activity.

    Args:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Output DataFrame
    """

    df_day = _get_day_percentage(df)

    if calendar is not None:
        df = df[df.Calendar == calendar]
        index = "SUMMARY"
    else:
        index = "Calendar"

    df = df.filter([index, "Duration"])

    df_sum = df.groupby(index).sum()
    # df_std["Duration"] = df_std["Duration"].fillna(0)
    # Float to int
    df_sum = df_sum.astype("int")
    # df_std = df_std.astype("int")
    # df = pd.concat([df_sum, df_std], axis=1)
    # print("df_sum", df_sum.dtypes)
    # print("df_day", df_day)
    df = pd.concat([df_sum, df_day], axis=1)
    df.columns = ["Activities Count", "% of days"]
    df.sort_values(by="Activities Count", ascending=False, inplace=True)
    st.table(df)


def _get_day_percentage(df):
    """Get dataframe with percentage of days covered by an activity.

    Returns:
                           DAY
    Calendar
    Chores               54.8%
    Commute              63.9%
    Eat                  99.9%
    """
    df = df.filter(["Calendar", "DAY"])
    df = df.drop_duplicates()
    df_day = df.groupby(["Calendar"]).count()
    # Normalize by total days, e.g. Eat: 1126 / 1127 = 0.999113
    df_day["DAY"] /= len(df["DAY"].unique())
    # Float to percentage, e.g. Eat: 0.999113 -> 99.9%
    df_day["DAY"] = df_day["DAY"].astype(float).map("{:.1%}".format)
    return df_day
