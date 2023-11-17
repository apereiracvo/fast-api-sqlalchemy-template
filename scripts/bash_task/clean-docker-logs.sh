#!/bin/bash

# Clear Docker logs for a specified container
CONTAINER_NAME=$1
LOG_PATH=$(docker inspect --format='{{.LogPath}}' "$CONTAINER_NAME")

if [ -n "$LOG_PATH" ]; then
  echo "Container: " $CONTAINER_NAME
    echo "Cleaning Log: "$LOG_PATH
    sudo truncate -s 0 "$LOG_PATH"
else
    echo "Log path not found for container $CONTAINER_NAME"
fi
