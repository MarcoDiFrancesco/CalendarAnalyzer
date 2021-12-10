import altair as alt
import pandas as pd

calendars = {
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


def legend(df: pd.DataFrame) -> alt.Scale:
    """Return altair legend with only the calendar that appear on
    the dataframe in column Calendar
    """
    # Names
    domain = []
    # Colors
    range = []
    cal_names = df["Calendar"].unique()
    for name in cal_names:
        domain.append(name)
        range.append(calendars[name])
    return alt.Scale(domain=domain, range=range)
