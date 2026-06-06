Overview

# Taxi Trip API Development

Taxi Trip API is a FastAPI + PostgreSQL application developed as part of an MLOps/LLMOps Bootcamp assignment. The project provides user authentication, taxi trip management, CSV dataset import and automated integration testing.

## Features

- User registration
- User login
- JWT authentication
- Bcrypt password hashing
- Public trip retrieval: `GET /trips`
- Protected trip creation: `POST /trips`
- PostgreSQL database
- CSV seed insert, one row at a time
- Curl-based test script
- Full workflow automation with shell scripts

## Project Structure

```text
TaxiTripAPI/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── trips.py
│   └── utils/
│       └── bulk_insert.py
├── data/raw/taxi-trip-data.csv
├── scripts/
│   ├── db.sh
│   ├── fastapi.sh
│   ├── bulk_insert.sh
│   ├── test_api.sh
│   ├── run-all.sh
│   └── reset-all.sh
├── reports/test_report.txt
├── docker-compose.yml
├── .env
└── README.md
```

## Environment Variables (.env)

Create .env in the project root:

```text
SQLALCHEMY_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/taxitrip_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Run 

If you cloned the project from GitHub, this step is already saved in Git.
You may run the command below if you face any permission warning or error!

- Give Execution Permission:

```text
chmod +x scripts/*.sh 
```

- Run full workflow:

```text
./scripts/run-all.sh
```

**This command:**

1. Starts PostgreSQL
2. Waits for PostgreSQL readiness
3. Starts FastAPI
4. Waits for API readiness
5. Inserts CSV rows into PostgreSQL one by one
6. Runs API tests

- Reset if you face any problem or make mistake you may use reset command below:

```text
./scripts/reset-all.sh

```
then run again all :

```text
./scripts/run-all.sh

```


## Scripts

| Script | Purpose |
|----------|-----------------------------------------------|
| `scripts/db.sh` | Starts PostgreSQL container |
| `scripts/fastapi.sh` | Starts the FastAPI application |
| `scripts/bulk_insert.sh` | Imports CSV records into PostgreSQL |
| `scripts/test_api.sh` | Runs API integration tests using `curl` |
| `scripts/run-all.sh` | Executes the complete project workflow |
| `scripts/reset-all.sh` | Cleans up the local development environment |

---

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|----------|---------------------|:-------------:|-------------------------------------------|
| `GET` | `/` | No | Health check endpoint |
| `POST` | `/register` | No | Register a new user |
| `POST` | `/login` | No | Authenticate user and receive JWT token |
| `GET` | `/trips?limit=10` | No | Retrieve taxi trip records |
| `POST` | `/trips` | Yes | Create a new trip record |
| `GET` | `/trips/{row_id}` | Yes | Retrieve a specific trip by ID |

## Expected Test Results

With running this code:
```text

./scripts/run-all.sh
```
Shoul show :

- Inserted rows: 5
- POST /register -> 201 Created
- POST /login -> 200 OK
- GET /trips without token -> 200 OK
- POST /trips without token -> 401 Unauthorized
- POST /trips with token -> 200 OK
- Invalid body -> 422 Unprocessable Entity
- GET /trips/999999 -> 404 Not Found

## Database Verification

After the full test workflow:

```text
docker exec -it taxitrip_db psql -U postgres -d taxitrip_db -c "SELECT COUNT(*) FROM taxitrips;"
```
Expected result:

```text
count
-----
6
```

Explanation:

```text
5 records inserted from CSV
+1 record created through POST /trips test
=6 total records
```

## Test Report:

```text
reports/test_report.txt
```
## Swagger Outputs:

- Successful Register:

```text
{
  "username": "Ozkan",
  "email": "ozkan@test.com",
  "password": "323232pk"
}
```
<p align="center">
<img src="reports/screenshots/2_register_new_user.png" width="900">
</p>

![Register Success](reports/screenshots/2_register_new_user.png)


- Duplicate User Name:

```text
{
  "username": "Ozkan",
  "email": "o.zkan@test.com",
  "password": "323232fk"
}
```

<img src="reports/screenshots/3_register_usernameexists.png" height ="400" width="600">

- Login & JWT Token:

```text
{
  "username": "Ozkan",
  "password": "323232pk"
}
```

<img src="reports/screenshots/5_login_successfulwithMin username.png" height ="400" width="600">



## Swagger Docs:

After starting API:

```text
http://127.0.0.1:8001/docs
```

## Notes

- GET /trips is public as required.
- POST /trips requires JWT authentication.
- Passwords are hashed with bcrypt.
- Input validation is handled with SQLModel/Pydantic schemas.
- CSV records are inserted one by one.