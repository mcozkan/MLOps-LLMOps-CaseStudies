import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

# get connection string from .env
load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
print(SQLALCHEMY_DATABASE_URL)

# Define an engine in order to start connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)

# start connection engine :
def get_db():
    db = Session(engine) # session creation
    try:
        # yield ensures database connections are always properly closed, preventing memory leaks and connection pool exhaustion.
        yield db
        # Route uses the session...
        # Route finishes...
    finally:
        db.close()
