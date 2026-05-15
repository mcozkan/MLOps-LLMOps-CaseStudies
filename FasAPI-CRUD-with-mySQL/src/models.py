from typing import Optional
from sqlmodel import SQLModel, Field

# Create Table customers
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
    customerId: int
    customerFName: str
    customerLName: str
    customerEmail: str
    customerPassword: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str

# PUT Validation:
# Their types are defined as Optional because CustomerUpdate should allow partial updates.
class CustomerUpdate(SQLModel):
    customerFName: Optional[str] = None
    customerLName: Optional[str] = None
    customerEmail: Optional[str] = None
    customerPassword: Optional[str] = None
    customerStreet: Optional[str] = None
    customerCity: Optional[str] = None
    customerState: Optional[str] = None
    customerZipcode: Optional[str] = None



# RESPONSE:
class CustomerRead(SQLModel):
    customerId: int
    customerFName: str
    customerLName: str
    customerEmail: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str
