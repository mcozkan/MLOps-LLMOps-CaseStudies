#!/bin/bash

set -e

BASE_URL="http://127.0.0.1:8001"

echo "1. Health check"
curl -i "$BASE_URL/"

echo -e "\n\n2. Register user"
curl -i -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "test123"
  }'

echo -e "\n\n3. Login user and get token"
TOKEN=$(curl -s -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}' | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
  echo "ERROR: Login failed. Token could not be retrieved."
  exit 1
fi

echo "TOKEN received."

echo -e "\n\n4. Public retrieval test - GET /trips without token"
curl -i "$BASE_URL/trips?limit=5"

echo -e "\n\n5. Security test - POST /trips without token should fail"
curl -i -X POST "$BASE_URL/trips" \
  -H "Content-Type: application/json" \
  -d '{
    "VendorID": 1,
    "tpep_pickup_datetime": "2024-01-01T10:00:00",
    "tpep_dropoff_datetime": "2024-01-01T10:20:00",
    "passenger_count": 1,
    "trip_distance": 3.5,
    "RatecodeID": 1,
    "store_and_fwd_flag": "N",
    "PULocationID": 100,
    "DOLocationID": 200,
    "payment_type": 1,
    "fare_amount": 15.5,
    "extra": 1.0,
    "mta_tax": 0.5,
    "tip_amount": 2.0,
    "tolls_amount": 0.0,
    "improvement_surcharge": 0.3,
    "total_amount": 19.3,
    "congestion_surcharge": 2.5,
    "Airport_fee": 0.0
  }'

echo -e "\n\n6. Create trip with token"
curl -i -X POST "$BASE_URL/trips" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "VendorID": 1,
    "tpep_pickup_datetime": "2024-01-01T10:00:00",
    "tpep_dropoff_datetime": "2024-01-01T10:20:00",
    "passenger_count": 1,
    "trip_distance": 3.5,
    "RatecodeID": 1,
    "store_and_fwd_flag": "N",
    "PULocationID": 100,
    "DOLocationID": 200,
    "payment_type": 1,
    "fare_amount": 15.5,
    "extra": 1.0,
    "mta_tax": 0.5,
    "tip_amount": 2.0,
    "tolls_amount": 0.0,
    "improvement_surcharge": 0.3,
    "total_amount": 19.3,
    "congestion_surcharge": 2.5,
    "Airport_fee": 0.0
  }'

echo -e "\n\n7. Get trips after authenticated creation"
curl -i "$BASE_URL/trips?limit=10"

echo -e "\n\n8. Validation test - invalid trip body"
curl -i -X POST "$BASE_URL/trips" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"trip_distance": "wrong_type"}'

echo -e "\n\n9. Error handling - trip not found"
curl -i "$BASE_URL/trips/999999" \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\n10. Performance sanity check - public retrieval"
time curl -s "$BASE_URL/trips?limit=10" > /dev/null