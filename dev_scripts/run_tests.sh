#!/bin/bash

export DB_HOST=localhost
export DB_DATABASE=primary_db
export DB_USER=user
export DB_PASSWORD=password
export DB_PORT=5432
export DB_ENGINE=django.db.backends.postgresql
export SECRET_KEY='django-insecure-0((h29a37al@^re@e!a#jclgqzdo2j!j&4t-!b8(-5#)=kf@e!'
export DEBUG=1
export DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1] *"
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@admin.com
export DJANGO_SUPERUSER_PASSWORD=password
export CORS_ALLOWED_ORIGINS="http://localhost:3000,http://localhost"

# Check if running inside a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Running inside a virtual environment"
else
    echo "Not running inside a virtual environment"
    exit 1
fi

# Navigate to the backend directory
cd backend || { echo "Failed to navigate to the backend directory"; echo "Make sure you're running from repo root"; exit 1; }

# Run tests
#python manage.py test socialnetwork.tests.test_follow
python manage.py test