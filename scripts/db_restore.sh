#!/bin/bash

# Get the container ID
container_id=$(docker ps --filter "name=sample-db" --format "{{.ID}}")

# Prompt the user for the backup file name
read -p "Enter the name of the backup file (e.g., backup.sql): " backup_file

# Copy the backup file to the temporary directory inside the container
docker cp "$(pwd)/$backup_file" $container_id:/tmp/backup.sql

# Restore the backup
docker exec -t $container_id psql -U postgres -d postgres -f /tmp/backup.sql

# Cleanup: Remove the backup file from the container
docker exec -t $container_id rm /tmp/backup.sql
