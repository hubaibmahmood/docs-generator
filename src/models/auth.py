
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """Represents a user."""
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    """Represents a user in the database (with hashed password)."""
    hashed_password: str

class Token(BaseModel):
    """Represents a JWT token."""
    access_token: str
    token_type: str

class TokenWithUser(Token): # New model
    """Represents a JWT token along with user details."""
    user_name: str # The name to display on the frontend
