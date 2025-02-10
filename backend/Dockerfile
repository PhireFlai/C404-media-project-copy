# filepath: backend/Dockerfile
FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev gdal-dev geos-dev
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]