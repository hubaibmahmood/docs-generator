from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables before importing other modules that might rely on them
load_dotenv()

from . import routes

app = FastAPI(
    title="Code Analysis Engine API",
    description="An API for analyzing remote Git repositories.",
    version="1.0.0",
)

app.include_router(routes.router)

@app.get("/")
async def read_root():
    """
    Root endpoint to verify the service is running.
    """
    return {"message": "Welcome to the Code Analysis Engine API"}
