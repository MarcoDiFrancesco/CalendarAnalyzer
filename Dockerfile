FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y gcc
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -U pip wheel setuptools
RUN pip install --timeout 120 -r requirements.txt
COPY . .
CMD streamlit run app.py --client.showErrorDetails=false
