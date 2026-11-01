#!/bin/bash
set -euo pipefail

IMAGE_NAME="fastapi-app"
CONTAINER_NAME="fastapi-app-container"
PORT="8000"

echo "Starting automatic deployment..."

echo "Building Docker image: ${IMAGE_NAME}..."
docker build -t "${IMAGE_NAME}" .

if [ -n "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
    echo "Stopping and removing the old container..."
    docker stop "${CONTAINER_NAME}"
    docker rm "${CONTAINER_NAME}"
fi

echo "Running container on port ${PORT}..."
docker run -d \
    -p "${PORT}:${PORT}" \
    --name "${CONTAINER_NAME}" \
    -v sqlite_data:/app/data \
    "${IMAGE_NAME}"

echo "Container successfully started!"
docker ps -f name="${CONTAINER_NAME}"