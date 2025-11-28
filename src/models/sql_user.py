from sqlalchemy import Boolean, Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
