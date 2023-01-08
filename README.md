<h1 align="center">Welcome to Calendar Analyzer 👋</h1>

> My life, visualized.

Visualize **Google Calendar** events in an **Interactive Dashboard**.

<p align="center">
<kbd>
    <img src="img/calendar-to-streamlit.png" width=100%>
</kbd>
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

## Data collection

Done using Google Calendar

<p align="center">
<kbd>
    <img src="img/google-calendar-week-view.png" width=600>
</kbd>
</p>

## Dashboard

<p align="center">
<!-- All activities -->
<img src="img/all-activities.png" width=600 />

<kbd align="center">
    <!-- Single activity -->
    <img src="https://i.imgur.com/uX8VCSD.png" width=600 />

</kbd>

<kbd align="center">
    <!-- Workout -->
    <img src="https://i.imgur.com/YF3F5up.png" width=600 />
</kbd>
</p>
````
