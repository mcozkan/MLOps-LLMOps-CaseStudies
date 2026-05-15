from typing import Optional, List
from sqlmodel import SQLModel, Field, Column


class Customer(SQLModel, table = True):
    __tablename__ = "customers"
    customerId: Optional[int] = Field(default=None, primary_key=True)
    customerFName: str
    customerLName: str
    customerEmail: str
    customerPassword: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str

# POST Validation:
class CustomerCreate(SQLModel):


# PUT Validation:
class CustomerUpdate(SQLModel):


# RESPONSE:
class CustomerRead(SQLModel):
