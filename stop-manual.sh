#!/bin/bash
set -euo pipefail

CONTAINER_NAME="fastapi-app-container"

echo "Stopping Docker container..."

if [ -n "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
    echo "Stopping container ${CONTAINER_NAME}..."
    docker stop "${CONTAINER_NAME}" >/dev/null

    echo "Removing container ${CONTAINER_NAME}..."
    docker rm "${CONTAINER_NAME}" >/dev/null

    echo "Docker container successfully stopped and removed."
else
    echo "Container ${CONTAINER_NAME} is not running or does not exist."
fi