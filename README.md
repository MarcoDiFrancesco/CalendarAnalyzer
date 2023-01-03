# Calendar Analyzer

My life, visualized.

## How to run

```sh
# (Optional) Create Virtual Environment
python -m venv .venv
# (Optional) Source Virtual Environment
source .venv/bin/activate
# Install wheels to speedup install
pip install wheel
# Install packages
pip install -r requirements.txt
# Source environment variable
source .envvars.sample
# Run Dashboard
streamlit run app.py
# Now open: http://localhost:8501
```

## Data collection

Done using Google Calendar

<p align="center">
<kbd>
    <img src="img/google-calendar-week-view.png" width=600>
</kbd>
</p>

## Dashboard

Preview: [http://raspberry.gleeze.com:8501](http://raspberry.gleeze.com:8501)

(hosted in a 1GB Raspberry Pi, be kind to it ❤️)

<p align="center">
<kbd>
    <!-- All activities -->
    <img src="https://i.imgur.com/KNwPSST.png" width=600 />
</kbd>

<kbd align="center">
    <!-- Single activity -->
    <img src="https://i.imgur.com/uX8VCSD.png" width=600 />

</kbd>

<kbd align="center">
    <!-- Workout -->
    <img src="https://i.imgur.com/YF3F5up.png" width=600 />
</kbd>
</p>
