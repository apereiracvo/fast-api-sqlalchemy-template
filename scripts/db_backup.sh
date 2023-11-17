#!/bin/bash

# Get the container ID
container_id=$(docker ps --filter "name=sample-db" --format "{{.ID}}")

# Create the backup
docker exec -t $container_id pg_dump -U postgres postgres > /tmp/backup.sql

# Copy the backup to the current working directory
cp /tmp/backup.sql "$(pwd)/backup.sql"

# Cleanup: Remove the backup file from the container
rm /tmp/backup.sql
