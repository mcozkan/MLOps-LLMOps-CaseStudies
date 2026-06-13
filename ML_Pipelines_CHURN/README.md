# ML Pipelines - Churn Prediction API

A simple end-to-end Machine Learning pipeline project that trains a customer churn prediction model and serves predictions through a FastAPI application.

This project demonstrates:

- Data loading and preprocessing
- Machine Learning model training with Scikit-Learn
- Model serialization using Joblib
- REST API development with FastAPI
- Containerization with Docker
- Dependency management with UV

---

# Project Structure

```text
ML_PIPELINES_CHURN/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── train_model.py
│   └── model.joblib
│
├── data/
│   └── raw/
│       └── Churn_Modelling.csv
│
│
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── README.md
├── .dvcgitignore
└── .gitignore
```

---

# Dataset

This project uses the Bank Customer Churn dataset.

## Target Variable

```text
Exited
```

## Features

```text
CreditScore
Geography
Gender
Age
Tenure
Balance
NumOfProducts
HasCrCard
IsActiveMember
EstimatedSalary
```

---

# Model Training

The training pipeline performs:

### Numerical Feature Scaling

```python
StandardScaler()
```

### Categorical Feature Encoding

```python
OneHotEncoder(handle_unknown="ignore")
```

### Classification Model

```python
RandomForestClassifier(random_state=42)
```

The preprocessing and model training steps are combined using a Scikit-Learn Pipeline.

To train the model manually:

```bash
python app/train_model.py
```

After training, the model is saved as:

```text
app/model.joblib
```

---

# API Endpoints

## Health Check

### Request

```http
GET /
```

### Response

```json
{
  "message": "Bank Churn Prediction API is running"
}
```

---

## Predict Churn

### Request

```http
POST /predict
```

### Request Body

```json
{
  "CreditScore": 619,
  "Geography": "France",
  "Gender": "Female",
  "Age": 42,
  "Tenure": 2,
  "Balance": 0,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 101348.88
}
```
<p align="center">
<img src="screenshots/1_predicition_input_try.png" width="700">
</p>


### Response

```json
1
```

<p align="center">
<img src="screenshots/2_prediciton_output.png" width="700">
</p>

Where:

```text
0 = Customer stays
1 = Customer churns
```

---

# Installation

## Clone Repository

```bash
git clone <repository_url>
cd ML_PIPELINES_CHURN
```

## Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

Using UV:

```bash
pip install uv
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Train the Model

```bash
python app/train_model.py
```

## Start the API

```bash
uvicorn app.main:app --reload --port 8502
```

Swagger UI:

```text
http://localhost:8502/docs
```

---

# Docker

## Build Docker Image

```bash
docker build -t churn-prediction-api .
```

## Run Docker Container

```bash
docker run -p 8502:8502 churn-prediction-api
```

API Documentation:

```text
http://localhost:8502/docs
```

---

# Technologies

- Python 3.12
- FastAPI
- Scikit-Learn
- Pandas
- Joblib
- Docker
- Uvicorn
- Pydantic
- UV

---

# Future Improvements

- Model versioning with DVC
- Experiment tracking with MLflow
- Automated retraining pipeline
- Unit and integration tests
- CI/CD pipeline
- Model monitoring and observability
- Feature store integration

---

# Author

**Murat Çağrı Özkan**

Data Scientist | Machine Learning Engineer | MLOps Enthusiast
