from pydantic import BaseModel, EmailStr
from enum import Enum

# Enum for user roles
class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.USER  # Default to 'user' role

# Schema for outputting user details
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum  # Include user role in the output

    class Config:
        orm_mode = True

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for authentication tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data (used during authentication)
class TokenData(BaseModel):
    email: str | None = None
