#!/bin/bash

set -e

echo "Starting data insertion - bulk insert..."

python -m app.utils.bulk_insert

echo "Data insertion completed!"