#!/bin/bash
set -euo pipefail

echo "Stopping and cleaning up containers..."
docker compose down 
    
echo "All containers stopped and removed, isolated network cleaned up."