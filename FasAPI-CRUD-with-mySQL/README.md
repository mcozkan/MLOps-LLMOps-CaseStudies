## MySQL Docker Setup

### 1. Start MySQL Container

Use the following command to start the MySQL container using the provided `docker-compose.yaml` file:

```bash
docker compose up -d
```

![mysql_db_on_docker.png](artifacts/screenshots/mysql_db_on_docker.png)

### 2. Connect to the MySQL Container

```bash
docker exec -it fastapi_crud_mysql mysql -u root -p
```



### 3. Create the mlops Database

```bash
CREATE DATABASE mlops;
```

<img src="artifacts/screenshots/create_db_mlops.png" hight ="100" width="300"/>

### 4. Create the mlops_user

```bash
CREATE USER 'mlops_user'@'%' IDENTIFIED BY 'your_password';
```

### 5. Grant Privileges to mlops_user

```bash
GRANT ALL PRIVILEGES ON mlops.* TO 'mlops_user'@'%';

FLUSH PRIVILEGES;
```
![create_user_give_privileges.png](artifacts/screenshots/create_user_give_privileges.png)

### 6. Verify Databases and Users
#### Show Database List
```bash
SHOW DATABASES;
```
#### Show Database List
```bash
SELECT user, host FROM mysql.user;
```

## Dataset

The dataset was downloaded into the `data/raw` directory using:

```bash
wget https://raw.githubusercontent.com/erkansirin78/datasets/master/retail_db/customers.csv
```

This project is part of the `MLOps-LLMOps-CaseStudies` monorepo.  
DVC was initialized with `--subdir` because the project lives inside a parent Git repository.

```bash
dvc init --subdir
```
### Before running the FastAPI application, make sure the MySQL container is running:

```bash
docker compose up -d
```

## Install Requirements

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Run the FastAPI Application

Start the FastAPI application with:

```bash
uvicorn src.main:app --reload --port 8001
```

After the application starts successfully, Swagger UI will be available at:

```text
http://127.0.0.1:8001/docs
```
<img src="artifacts/screenshots/swagger_root_success.png" hight ="250" width="250"/>

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/customers` | Create a new customer |
| GET | `/customers` | List customers with optional filtering |
| GET | `/customers/{customer_id}` | Get a customer by ID |
| PUT | `/customers/{customer_id}` | Update a customer |
| DELETE | `/customers/{customer_id}` | Delete a customer |

---

# Password Hashing

Customer passwords are hashed using `passlib` and `bcrypt` before being stored in the database.

Example hashed password stored in MySQL:

![hashed_passwords_mysql.png](artifacts/screenshots/first_customer_insert_by_swagger_in_db.png)

---

# Insert First 10 Rows via API

The first 10 rows of the dataset were inserted into the database using the custom FastAPI POST endpoint and a Python seeding script.

Run the script with:

```bash
python seed_data.py
```

![seed_data_script.png](artifacts/screenshots/10_customers_seed_data_insert.png)
![seed_data_script.png](artifacts/screenshots/10_customers_seed_data_insert_on_db.png)

---

# Filtering Example

Example request:

```text
GET /customers?city=Caguas&limit=3
```

This endpoint returns a limited number of customers filtered by city.


<img src="artifacts/swagger_screens/city_Caguas-limit_3.png" hight ="100" width="250"/>

---

# Update Example

Example update request:

```text
PUT /customers/8
```

Example:
- Previous lastname: `Smith`
- Updated lastname: `Fox`

![update_customer_fox.png](artifacts/screenshots/update_customer_fox.png)

---

# Delete Example

Example delete request:

```text
DELETE /customers/4
```

After deletion, customer with ID 4 no longer exists in the database.

![delete_customer.png](artifacts/screenshots/delete_customer.png)

---

# Technologies Used

- FastAPI
- SQLModel
- MySQL
- Docker
- Pandas
- Requests
- Passlib
- bcrypt
- DVC

---

# Project Structure

```text
FasAPI-CRUD-with-mySQL/
│
├── artifacts/
├── data/
├── src/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── security.py
│
├── seed_data.py
├── docker-compose.yaml
├── requirements.txt
├── .gitignore
└── README.md
```