from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import auth, trips

app = FastAPI(title="Taxi Trip API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth.router)
app.include_router(trips.router)


@app.get("/")
def root():
    return {"message": "Taxi Trip API is running"}