FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y gcc
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install "pip>=22.1.2,<22.2.0" wheel setuptools
RUN pip install -r requirements.txt --timeout 120 --use-deprecated=backtrack-on-build-failures
COPY . .
CMD streamlit run app.py --client.showErrorDetails=false
