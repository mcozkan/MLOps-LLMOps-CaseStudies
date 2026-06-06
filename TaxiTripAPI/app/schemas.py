from typing import Optional
from pydantic import constr
from sqlmodel import SQLModel, Field
from datetime import datetime



############################################ Base Models ############################################ 
# Base model for all TaxiTrip-related schemas and database models
class TaxiTripBase(SQLModel):
    VendorID: int = Field(description= 'Identifier for the vendor providing the trip data')
    tpep_pickup_datetime: datetime = Field(description= 'Date and time when the trip started')
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


########################################### Pydantic Schemas for API ############################################

# Pydantic schema for creating a new TaxiTrip record (used in POST requests)
class TaxiTripCreate(TaxiTripBase):
    # Optional field for row_id, can be generated automatically if not provided
    row_id: Optional[str] = Field(default=None, description="Optional unique identifier. Generated automatically if omitted.")  


# Pydantic schema for reading a TaxiTrip record (used in GET requests)
class TaxiTripRead(TaxiTripBase):
    row_id: str = Field(description= 'Unique identifier for each row (e.g., a hash of row values or int)')

# Pydantic schema for user login (used in POST requests for authentication)
class UserLogin(SQLModel):
    username: str = Field(description= 'Username for the user (used for authentication)')
    password: constr(min_length=4, max_length=72) = Field(description= 'Password for the user (used for authentication)')

# Pydantic schema for creating a new User (used in POST requests)
class UserCreate(UserBase):
    password: constr(min_length=4, max_length=72) = Field(description= 'Password for the user (will be hashed before storing)')


# Pydantic schema for reading a User (used in GET requests)
class UserRead(UserBase):
    id: int = Field(description= 'Unique identifier for the user')

# Pydantic schema for representing an authentication token (used in responses after successful login)
class Token(SQLModel):
    access_token: str = Field(description= 'JWT access token for authentication')
    token_type: str = Field(default="bearer", description="Authentication scheme") 


