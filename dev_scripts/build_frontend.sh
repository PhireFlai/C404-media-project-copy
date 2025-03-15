#!/bin/bash

# Check if running inside a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Running inside a virtual environment"
else
    echo "Not running inside a virtual environment"
    exit
fi

# Navigate to the frontend directory
cd frontend || { echo "Failed to navigate to the frontend directory"; echo "Make sure you're running from repo root"; exit 1; }

# Install npm dependencies
npm install

# Start the React development server
npm start