FROM python:3.7-slim

RUN pip install --upgrade pip

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
