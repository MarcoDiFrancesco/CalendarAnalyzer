import warnings

import altair as alt
import pandas as pd
import streamlit as st
from streamlit.commands.page_config import set_page_config

from utils import admin, clean_df
from utils.all_activities import chart_calendars, chart_calendars_longest
from utils.compute_day import compute_day
from utils.download_cals import download_cals
from utils.entertainment import entertainment
from utils.fix_activitires import fix_activities
from utils.single_activity import (
    chart_calendar_vert,
    chart_decreasing_activity,
    select_activity,
)
from utils.sport import chart_sport
from utils.study import chart_study_horiz, chart_study_vert
from utils.table_sum import table_sum

set_page_config(page_title="Calendar Analyzer", page_icon="⌛")
st.title("Calendar Analyzer")
st.caption(
    "[https://github.com/MarcoDiFrancesco/CalendarAnalyzer](https://github.com/MarcoDiFrancesco/CalendarAnalyzer)"
)

df = download_cals().copy()
df = clean_df.clean_df(df)

df = admin.get_password(df)
df = df.sort_values("DTSTART")
compute_day(df)
fix_activities(df)

# All activities
st.markdown("---")
st.header("All activities")
chart_calendars(df)
chart_calendars_longest(df)
table_sum(df)

# Selected activity
st.markdown("---")
st.header("Single activity")
st.text("Unique activities divided by calendar")
calendar = select_activity(df)
chart_calendar_vert(df, calendar)
chart_decreasing_activity(df, calendar)
table_sum(df, calendar)

# Sport
st.markdown("---")
st.header("Sport")
chart_sport(df)
entertainment(df)

# Study
st.markdown("---")
st.header("Study")
chart_study_vert(df)
chart_study_horiz(df)
entertainment(df)
