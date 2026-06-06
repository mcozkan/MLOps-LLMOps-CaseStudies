#!/bin/bash

set -e

echo "Starting FastAPI..."
# start the FastAPI server in the background
uvicorn app.main:app --reload --port 8001 &

# Wait for the server to start
sleep 5

echo "FastAPI is running on http://localhost:8001"
