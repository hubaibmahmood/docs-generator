from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    """Represents a user."""
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    """Represents a user in the database (with hashed password)."""
    hashed_password: str

class Token(BaseModel):
    """Represents a JWT token."""
    access_token: str
    token_type: str
