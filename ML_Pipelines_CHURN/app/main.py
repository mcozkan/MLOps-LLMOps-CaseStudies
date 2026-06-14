import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Bank Churn Prediction API")

model = joblib.load("app/model.joblib")


class ChurnRequest(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float


@app.get("/")
def root():
    return {"message": "Bank Churn Prediction API is running"}


@app.post("/predict")
def predict(data: ChurnRequest):
    input_df = pd.DataFrame([data.model_dump()])

    prediction = model.predict(input_df)[0]

    return int(prediction)