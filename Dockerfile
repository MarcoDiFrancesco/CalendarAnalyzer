FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y gcc
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --timeout 120 -r requirements.txt
COPY . .
CMD streamlit run app.py
