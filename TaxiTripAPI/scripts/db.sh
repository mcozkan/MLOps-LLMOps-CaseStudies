#!/bin/bash

set -e

echo "Starting PostgreSQL..."
# This script sets up the postgres database.
docker compose up -d 

echo "Waiting for PostgreSQL..."

until docker exec taxitrip_db pg_isready -U postgres; do
  echo "PostgreSQL is not ready yet..."
  sleep 2
done

echo "PostgreSQL is ready!"  