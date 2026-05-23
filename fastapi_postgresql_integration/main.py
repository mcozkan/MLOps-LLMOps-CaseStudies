from fastapi import FastAPI
from routers.iris import iris_ep
from routers.advertising import advertising_ep
from routers.llm import llm_ep

app = FastAPI(title="Deploy ML/AI with API")

app.include_router(iris_ep.router)
app.include_router(advertising_ep.router)
app.include_router(llm_ep.router)

@app.get("/")
async def root():
    return {'message':'Hello FastAPI!'}

