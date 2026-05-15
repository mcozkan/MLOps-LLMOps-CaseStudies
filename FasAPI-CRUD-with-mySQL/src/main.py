from fastapi import FastAPI, status, Depends
from models import Customer
from database import get_db, engine
from sqlmodel import Session, SQLModel


app = FastAPI()

# All Table Create
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/")
async def root():
    return {"message" : "Hello!!!"}


@app.get("/customers/{customer_id}")
async def get_customers(customer_id : int):
    return {"data" : f"Customer {customer_id} is created!!!"}

