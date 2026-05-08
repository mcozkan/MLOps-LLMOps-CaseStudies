import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

from models import customerRequests, requestClassifications

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insert_customer_requests(request : customerRequests):
    with Session(engine) as session:
        session.add(request)
        session.commit()

def insert_request_classifications(request : requestClassifications):
    with Session(engine) as session:
        session.add(request)
        session.commit()
