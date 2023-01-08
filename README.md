<h1 align="center">Welcome to Calendar Analyzer 👋</h1>

> My life, visualized.

Visualize **Google Calendar** events in an **Interactive Dashboard**.

<p align="center">
<!-- <kbd> -->
<img src="img/calendar-to-streamlit.png" width=700>
<!-- </kbd> -->
</p>

<!-- ![img/calendar-to-streamlit.png](img/calendar-to-streamlit.png) -->

## [👁️ Preview](http://raspberry.gleeze.com:8501)

[Preview](http://raspberry.gleeze.com:8501) hosted in a 1GB Raspberry Pi, be kind to it ❤️

<p align="center">
<kbd><img src='img/preview1.png' width=250 /></kbd>
<!-- <kbd><img src='img/preview2.png' width=250 /></kbd> -->
<kbd><img src='img/preview3.png' width=250 /></kbd>
<!-- <kbd><img src='img/preview4.png' width=250 /></kbd> -->
<!-- <kbd><img src='img/preview5.png' width=250 /></kbd> -->
<kbd><img src='img/preview6.png' width=250 /></kbd>
</p>

<p align="center">
</p>

## 🚀 Usage

0. (Optional) Create Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate
```

1. Install Python packages

```sh
pip install wheel
pip install -r requirements.txt
```

2. Source environment variable (e.g. Calendar links)

```sh
source .envvars.sample
```

3. Run Dashboard

```sh
streamlit run app.py
```

4. Now open the Dashboard → localhost:8501

## Data collection strategy

Data is collected by adding events to Google Calendar.

**Structure** of these calendars (e.g. Study, Sport) can be found in [Categorization](https://github.com/MarcoDiFrancesco/CalendarAnalyzer/wiki/Categories) wiki page.

**Link** to download of the calendar instruction in [Get calendar link](https://github.com/MarcoDiFrancesco/CalendarAnalyzer/wiki/Get-calendar-link) wiki page.

<p align="center">
<kbd>
    <img src="img/google-calendar-week-view.png" width=600>
</kbd>
</p>
