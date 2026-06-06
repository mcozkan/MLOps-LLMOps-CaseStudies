#!/bin/bash

set -e

echo "Stopping FastAPI processes..."
pkill -f "uvicorn app.main:app" || true

echo "Stopping and removing Docker containers..."
docker compose down -v

echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "Cleanup completed."
echo ""
echo "You can now restart the project with:"
echo "./scripts/run-all.sh"