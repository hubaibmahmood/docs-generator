from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

@app.get("/")
async def read_root():
    """
    Root endpoint to verify the service is running.
    """
    return {"message": "Welcome to the Code Analysis Engine API"}
