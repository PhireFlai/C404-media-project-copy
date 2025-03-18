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
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@admin.com
export DJANGO_SUPERUSER_PASSWORD=password
export CORS_ALLOWED_ORIGINS="http://localhost:3000,http://localhost:80,http://localhost,http://[2605:fd00:4:1001:f816:3eff:fe04:65df],http://[2605:fd00:4:1001:f816:3eff:fe04:65df]:8000"

# Check if running inside a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Running inside a virtual environment"
else
    echo "Not running inside a virtual environment"
    exit 1
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

# Drop and recreate the database
# echo "Dropping and recreating the database..."
# docker exec db psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_DATABASE;"
# docker exec db psql -U $DB_USER -d postgres -c "CREATE DATABASE $DB_DATABASE;"

# Run migrations
python3 manage.py makemigrations --merge
python3 manage.py makemigrations
python3 manage.py makemigrations socialnetwork
python3 manage.py migrate

# Create superuser (optional, auto-generated)
# echo "Creating superuser..."
# echo "from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
#     User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
# " | python3 manage.py shell

# Launch the Django development server
python3 manage.py runserver
