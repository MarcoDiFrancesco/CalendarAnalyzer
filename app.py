import streamlit as st
from streamlit.commands.page_config import set_page_config

from utils import admin, clean_df
from utils.all_activities import chart_calendars, chart_calendars_longest
from utils.compute_day import compute_day
from utils.data_checks import data_checks
from utils.download_cals import download_cals
from utils.single_activity import single_activity_text
from utils.single_activity.chores import chores
from utils.single_activity.commute import commute
from utils.single_activity.eat import eat
from utils.single_activity.entertainment import entertainment
from utils.single_activity.personal_care import personal_care
from utils.single_activity.personal_development import personal_development
from utils.single_activity.sport import sport
from utils.single_activity.study import study
from utils.single_activity.work import work
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
    single_activity_text(df)
    chores(df)
    commute(df)
    eat(df)
    entertainment(df)
    personal_care(df)
    personal_development(df)
    sport(df)
    study(df)
    work(df)


if __name__ == "__main__":
    main()
