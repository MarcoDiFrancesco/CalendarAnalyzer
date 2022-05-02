FROM python:3.9-slim-buster
RUN apt-get update &&
    apt-get install -y --no-install-recommends gcc=4:8.3.* &&
    apt-get clean &&
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --timeout 120 -r requirements.txt
COPY . .
CMD streamlit run app.py --client.showErrorDetails=false
