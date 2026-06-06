# Taxi Trip API Development

Taxi Trip API is a FastAPI + PostgreSQL application developed as part of an MLOps/LLMOps Bootcamp assignment. The project provides user authentication, taxi trip management, CSV dataset import and automated integration testing.

## Technologies

- Python 3.12
- FastAPI
- SQLModel
- PostgreSQL
- Docker Compose
- JWT Authentication
- Passlib (bcrypt)
- Uvicorn
- Pydantic
- Bash

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
├── .venv/
├── .dvc/
│
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── trips.py
│   └── utils/
│       └── bulk_insert.py
│
├── data/raw/taxi-trip-data.csv
│
├── scripts/
│   ├── db.sh
│   ├── fastapi.sh
│   ├── bulk_insert.sh
│   ├── test_api.sh
│   ├── run-all.sh
│   └── reset-all.sh
│
├── reports/
│   ├──screenshots
│   ├──test_report.txt
│
├──docker-compose.yml
├──pyproject.toml
├──uv.lock
├──.python-version
├──.env
└── README.md
```

## Installation

1. Clone the repository:

```text
   git clone <repository_url>
   cd TaxiTripAPI
```

2. Create and activate a virtual environment:

```text
   python -m venv .venv
   source .venv/bin/activate      # Linux/Mac
   .venv\Scripts\activate         # Windows

```

3. Install project dependencies:

```text
   pip install uv
   uv sync
```

4. Create a .env file in the project root:

```text
   SQLALCHEMY_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/taxitrip_db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Pull the dataset using DVC:

```bash
dvc pull
```

## Data Version Control (DVC)

Large data files are tracked through DVC while keeping the Git repository lightweight.
Dataset location:

```text
data/raw/taxi-trip-data.csv
```

Common commands:

```bash
dvc pull      # Download tracked data
dvc status    # Check dataset status
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
<img src="reports/screenshots/2_register_new_user.png" width="700">
</p>

- Duplicate User Name:

```text
{
  "username": "Ozkan",
  "email": "o.zkan@test.com",
  "password": "323232fk"
}
```
<p align="center">
<img src="reports/screenshots/3_register_usernameexists.png" height ="400" width="600">
</p>


- Login & JWT Token:

```text
{
  "username": "Ozkan",
  "password": "323232pk"
}
```

<p align="center">
<img src="reports/screenshots/5_login_successfulwithMin username.png" height ="400" width="600">
</p>

You may find more screenshots on:

```text
reports/screenshots/
```

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

## Future Improvements

- Bulk CSV insertion optimization
- Dockerized API deployment
- Pytest-based automated testing
- CI/CD pipeline integration
- API versioning
- Pagination improvements

## Author

Murat Çağrı Özkan

GitHub:
https://github.com/...

Developed as part of the VBO MLOps / LLMOps Bootcamp.