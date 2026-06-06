from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


############################################ Base Models ############################################ 
# Base model for all TaxiTrip-related schemas and database models
class TaxiTripBase(SQLModel):
    VendorID : int = Field(description= 'Identifier for the vendor providing the trip data')
    tpep_pickup_datetime : datetime = Field(description= 'Date and time when the trip started')
    tpep_dropoff_datetime: datetime =  Field(description= 'Date and time when the trip ended')
    passenger_count: float = Field(description= 'Number of passengers in the trip')
    trip_distance: float = Field(description= 'Distance of the trip in miles')
    RatecodeID: float = Field(description= 'Rate code for the trip (e.g., standard, airport)')
    store_and_fwd_flag: str = Field(description= ' Flag indicating if the trip data was stored and forwarded (Y/N)')
    PULocationID: int = Field(description= 'Pickup location ID')
    DOLocationID: int = Field(description= 'Dropoff location ID')
    payment_type: int = Field(description= 'Payment method (e.g., 1 = credit card, 2 = cash) ')
    fare_amount: float = Field(description= 'Base fare for the trip')
    extra: float = Field(description= 'Extra charges (e.g., night surcharge)')
    mta_tax: float = Field(description= 'MTA tax applied to the trip')
    tip_amount: float = Field(description= 'Tip amount provided by the passenger')
    tolls_amount: float = Field(description= 'Tolls incurred during the trip')
    improvement_surcharge: float = Field(description= 'Surcharge for improvements')
    total_amount: float = Field(description= 'Total amount charged for the trip ')
    congestion_surcharge: float = Field(description= 'Congestion surcharge applied')
    Airport_fee: float = Field(description= 'Airport fee, if applicable')
    
# Base model for all Users-related schemas and database models
class UserBase(SQLModel):
    username: str
    email: Optional[str] = None


############################################ DB Tables Creates ############################################ 

# Inherited from tha TaxiTripBase model that it has been defined
class TaxiTrip(TaxiTripBase, table = True):
    __tablename__ = "taxitrips"
    row_id: Optional[str] = Field(default = None, primary_key= True, description= 'Unique identifier for each row (e.g., a hash of row values or int)')

# Inherited from tha UserBase model that it has been defined
class User(UserBase, table = True):
    __tablename__ = "users"
    id: Optional[int] = Field(default = None, primary_key = True)
    password_hash: str


