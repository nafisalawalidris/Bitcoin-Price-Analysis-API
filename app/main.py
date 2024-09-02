# main.py
from fastapi import FastAPI
from . import routes
from .database import engine
from .routes import router as price_router

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Include router
app.include_router(routes.router)
