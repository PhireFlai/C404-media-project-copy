#!/bin/bash

# filepath: /home/ubuntu/w25-project-cyan/dev_scripts/upload_default_pic.sh

# Define the file to upload and the target path inside the container
DEFAULT_PIC_PATH="backend/socialnetwork/media/profile_pictures/default.png"
TARGET_PATH="/app/socialnetwork/media/profile_pictures/"

# Check if the default picture exists
if [ ! -f "$DEFAULT_PIC_PATH" ]; then
    echo "Error: Default picture not found at $DEFAULT_PIC_PATH"
    exit 1
fi

# Identify the backend container
BACKEND_CONTAINER=$(docker ps --filter "name=w25-project-cyan-backend" --format "{{.ID}}")

# Check if the backend container is running
if [ -z "$BACKEND_CONTAINER" ]; then
    echo "Error: Backend container not found or not running."
    exit 1
fi

# Create the target directory inside the container (if it doesn't exist)
docker exec "$BACKEND_CONTAINER" mkdir -p "$TARGET_PATH"

# Copy the default picture into the container
docker cp "$DEFAULT_PIC_PATH" "$BACKEND_CONTAINER:$TARGET_PATH"

# Verify the file was copied successfully
docker exec "$BACKEND_CONTAINER" ls -l "$TARGET_PATH"

echo "Default picture successfully uploaded to $BACKEND_CONTAINER:$TARGET_PATH"