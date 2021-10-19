FROM python:3.7-buster

RUN pip install --upgrade pip


RUN mkdir /backend
WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt
