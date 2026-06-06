#!/bin/bash


set -e

echo "===== RUN-ALL STARTED ====="
# Run the database setup script
./scripts/db.sh

echo "===== DB DONE ====="

# Run the fastapi server script
./scripts/fastapi.sh &

echo "===== FASTAPI STARTED ====="

until curl -s http://127.0.0.1:8001 > /dev/null; do
    sleep 1
done

echo "Waiting for API startup..."

echo "===== API READY ====="

# Run the bulk insert script
./scripts/bulk_insert.sh

echo "===== BULK INSERT DONE ====="

# Run the API tests
./scripts/test_api.sh

echo "===== ALL DONE ====="
