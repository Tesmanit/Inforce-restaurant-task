FROM python:3.13.0-alpine3.20
COPY requirements.txt /temp/requirements.txt
COPY . /inforce_restaurant
WORKDIR /inforce_restaurant
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements.txt