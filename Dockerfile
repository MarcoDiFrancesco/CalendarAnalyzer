FROM python:3.9-slim-buster
EXPOSE 8501
WORKDIR /app
# RUN pip install wheel
COPY requirements.txt requirements.txt
RUN pip install --timeout 1000 -r requirements.txt
COPY . .
CMD streamlit run app.py
