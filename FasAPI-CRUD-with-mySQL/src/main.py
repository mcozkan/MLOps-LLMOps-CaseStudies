from fastapi import FastAPI, status, Depends
#from setuptools import depends
from src.models import CustomerCreate, Customer, CustomerRead, CustomerUpdate
from src.database import engine, get_db
from sqlmodel import SQLModel, Session, select
from typing import Optional, List
from src.security import hash_password


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

@app.post("/customers", response_model=CustomerRead,
          status_code=status.HTTP_201_CREATED)
async def create_customer(request: CustomerCreate, session: Session = Depends(get_db)):
    customer_data = request.model_dump()
    customer_data["customerPassword"] = hash_password(request.customerPassword)

    new_customer = Customer(**customer_data)

    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    # I removed `session.close()` because `get_db()` already handles opening and closing the database session automatically.

    return new_customer


@app.get("/customers", response_model=List[CustomerRead])
async def list_customers(
    city: Optional[str] = None,
    limit: int = 10,
    session: Session = Depends(get_db),
):
    statement = select(Customer)

    if city:
        statement = statement.where(
            Customer.customerCity == city
        )

    statement = statement.limit(limit)

    customers = session.exec(statement).all()

    return customers
'''
@app.post("/customers", response_model=List[CustomerRead])
async def 
'''