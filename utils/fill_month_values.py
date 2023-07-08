import datetime

import numpy as np
import pandas as pd


def fill_month_values(
    df: pd.DataFrame,
    month_col,
    value_col,
) -> pd.DataFrame:
    # e.g. ["2019-12", "2020-01", ...]
    # months = pd.date_range("2019-12", end=datetime.datetime.today(), freq="MS").strftime("%Y-%m")
    months = pd.date_range("2019-12", end="2022-12", freq="MS").strftime("%Y-%m")
    df_zeros = pd.DataFrame({month_col: months, value_col: np.zeros(len(months))})
    # Give priority to df, otherwise take df_zeros
    df_new = pd.concat([df, df_zeros])
    return df_new
