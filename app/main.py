from fastapi import FastAPI
from .database import engine
from . import models, routes

app = FastAPI()

# Include the API routers
app.include_router(routes.router)

@app.on_event("startup")
async def on_startup():
    # Initialize the database (only if needed; typically handled separately)
    from .init_db import init_db
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bitcoin Price API"}
