# filepath: backend/Dockerfile
FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

# RUN ls -l /app

CMD gunicorn socialnetwork.wsgi:application --bind [::]:8000 
