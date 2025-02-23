#!/bin/bash

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
python manage.py test