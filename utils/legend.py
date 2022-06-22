import altair as alt
import pandas as pd


def legend(
    df: pd.DataFrame, *, color_map: dict | None = None, column="Calendar"
) -> alt.Scale:
    """Return legend with only the calendar that appear on the dataframe in specified column.

    Args:
        df (pd.DataFrame): Input df
        color_map (dict, optional): {"Chores": "#7986CB", "Work": "#F09300"}
        column (str, optional): Calendar or SUMMARY. TODO: remove default

    Returns:
        alt.Scale: altair legend
    """
    if color_map is None:
        color_map = {
            "Chores": "#7986CB",
            "Commute": "#9E69AF",
            "Eat": "#039BE5",
            "Entertainment": "#F4511E",
            "Personal care": "#E67C73",
            "Personal development": "#F6BF26",
            "Spare time": "#B39DDB",
            "Sport": "#8E24AA",
            "Study": "#33B679",
            "Work": "#F09300",
        }

    # Names
    domain = []
    # Colors
    range = []
    cal_names = df[column].unique()
    for name in cal_names:
        domain.append(name)
        range.append(color_map.get(name, ""))
    return alt.Scale(domain=domain, range=range)
