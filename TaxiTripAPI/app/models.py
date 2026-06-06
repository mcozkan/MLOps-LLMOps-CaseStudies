from typing import Optional
from sqlmodel import Field
from app.schemas import TaxiTripBase, UserBase


# Inherited from tha TaxiTripBase model that it has been defined
class TaxiTrip(TaxiTripBase, table = True):
    __tablename__ = "taxitrips"
    row_id: Optional[str] = Field(default = None, primary_key= True, description= 'Unique identifier for each row (e.g., a hash of row values or int)')

# Inherited from tha UserBase model that it has been defined
class User(UserBase, table = True):
    __tablename__ = "users"
    id: Optional[int] = Field(default = None, primary_key = True)
    password_hash: str


