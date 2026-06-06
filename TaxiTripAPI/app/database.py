import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

#Create engine for the connection start.
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)

# create tables with the SQLModel if the class objects set as 'table = True'
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# open database connetion in order to do query operations
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()