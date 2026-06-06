#!/bin/bash

set -e

echo "Starting FastAPI..."
# start the FastAPI server in the background
uvicorn app.main:app --reload --port 8001
