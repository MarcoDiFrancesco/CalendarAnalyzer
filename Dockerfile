FROM python:3.9-slim-buster
EXPOSE 8501
WORKDIR /app
RUN apt-get update
RUN apt-get install -y gcc
COPY requirements.txt requirements.txt
RUN pip install --timeout 120 -r requirements.txt
COPY . .
CMD streamlit run app.py
