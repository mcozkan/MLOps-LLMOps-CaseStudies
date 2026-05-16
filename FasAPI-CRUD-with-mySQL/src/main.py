from fastapi import FastAPI, status, Depends, HTTPException
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

##########################################################################################################
@app.get("/customers/{customer_id}")
async def get_customers(customer_id : int):
    return {"data" : f"Customer {customer_id} is created!!!"}

# Creating Customers #####################################################################################
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

# Customer Filtering #####################################################################################
@app.get("/customers", response_model=List[CustomerRead], status_code=status.HTTP_200_OK)
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


# Customer Update #####################################################################################
@app.put("/customers/{customer_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer(customer_id: int, request: CustomerUpdate, session: Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, customer_id)
        if not one_customer:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"Customer with {id} has not found!")
        update_customer = request.model_dump(exclude_unset = True)
        one_customer.sqlmodel_update(update_customer)
        session.add(one_customer)
        session.commit()
        session.refresh(one_customer)
        return one_customer


# Customer Delete #####################################################################################
@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, session:Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, customer_id)
        if not one_customer:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"Customer with {id} has not found!")
        session.delete(one_customer)
        session.commit()
        return {f"Customer {id} deleted!"}



