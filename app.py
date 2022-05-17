import streamlit as st
from streamlit.commands.page_config import set_page_config

from utils import admin, clean_df
from utils.all_activities import chart_calendars, chart_calendars_longest
from utils.compute_day import compute_day
from utils.data_checks import data_checks
from utils.download_cals import download_cals
from utils.entertainment import entertainment
from utils.personal_development import personal_development
from utils.single_activity import (
    chart_calendar_vert,
    chart_decreasing_activity,
    print_text,
    select_activity,
)
from utils.sport import chart_sport
from utils.study import study
from utils.table_sum import table_sum


def main() -> None:
    set_page_config(page_title="Calendar Analyzer", page_icon="⌛")
    st.title("Calendar Analyzer")
    st.caption(
        "[https://github.com/MarcoDiFrancesco/CalendarAnalyzer](https://github.com/MarcoDiFrancesco/CalendarAnalyzer)"
    )

    df = download_cals().copy()
    df = clean_df.clean_df(df)

    compute_day(df)
    data_checks(df)

    df = admin.get_password(df)

    # All activities
    st.markdown("---")
    st.header("All activities")
    chart_calendars(df)
    chart_calendars_longest(df)
    table_sum(df)

    # Single activity
    print_text(df)
    calendar = select_activity(df)
    chart_calendar_vert(df, calendar)
    chart_decreasing_activity(df, calendar)
    table_sum(df, calendar)

    # Study
    study(df)
    # Personal development
    personal_development(df)
    # Entertainment
    entertainment(df)

    # Sport
    st.markdown("---")
    st.header("Sport")
    chart_sport(df)


if __name__ == "__main__":
    main()
