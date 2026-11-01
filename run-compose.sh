#!/bin/bash
set -euo pipefail

echo "Building and starting containers with Docker Compose..."
docker compose up -d --build

echo "----------------------------------------"
echo "System deployed successfully!"
echo "FastAPI API:    http://localhost:8000"
echo "SQLite Web GUI: http://localhost:8080"
echo "----------------------------------------"