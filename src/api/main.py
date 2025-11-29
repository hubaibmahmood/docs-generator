
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables before importing other modules that might rely on them
load_dotenv()

from . import auth, routes
from .auth import get_current_user_from_cookie

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

# Public Routes (Login)
app.include_router(auth.router, prefix="/auth")

# Protected Routes (Analysis)
# We use dependencies=[Depends(get_current_user_from_cookie)] to protect all routes in this router
app.include_router(routes.router, dependencies=[Depends(get_current_user_from_cookie)])

@app.get("/")
async def read_root():
    """
    Root endpoint to verify the service is running.
    """
    return {"message": "Welcome to the Code Analysis Engine API"}
