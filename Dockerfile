FROM python:3.13-alpine

RUN apk add git postgresql-dev python3-dev gcc libpq-dev postgresql

WORKDIR /code

RUN pip install --upgrade pip && pip install pipenv
ENV PIPENV_CUSTOM_VENV_NAME="products-api"
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --dev