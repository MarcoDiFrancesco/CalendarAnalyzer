import pandas as pd


def df_shorten_string(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Keep 2 words from the given column.

    From:
           Period  Calendar                           SUMMARY  Duration
    21    2019-12     Study    Formal languages and compilers      23.0
    To:
           Period  Calendar                           SUMMARY  Duration
    21    2019-12     Study                  Formal languages      23.0

    """
    df[col_name] = df[col_name].str.split(" ").str[:2].str.join(" ")
    return df
