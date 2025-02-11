#!/bin/bash

# Set environment variables
export DB_HOST=localhost
export DB_DATABASE=primary_db
export DB_USER=user
export DB_PASSWORD=password
export DB_PORT=5432
export DB_ENGINE=django.db.backends.postgresql
export SECRET_KEY='django-insecure-0((h29a37al@^re@e!a#jclgqzdo2j!j&4t-!b8(-5#)=kf@e!'
export DEBUG=1
export DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1] *"

# Check if running inside a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Running inside a virtual environment"
else
    echo "Not running inside a virtual environment"
    exit
fi

# Start the database container
docker compose up -d db

# Wait for the database to be ready
while ! docker exec db pg_isready -U $DB_USER -d $DB_DATABASE; do
    echo "Database still launching"
    sleep 2
done

# Navigate to the backend directory
cd backend || { echo "Failed to navigate to the backend directory"; echo "Make sure you're running from repo root"; exit 1; }

# Install dependencies from requirements.txt
pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

# Launch the Django development server
python3 manage.py runserver