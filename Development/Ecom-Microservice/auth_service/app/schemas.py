from typing import List, Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

# Enum for user roles
class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

# --- User Schemas ---

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
    permissions: List[str]  # Change this to a list of strings

    class Config:
        orm_mode = True

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Token Schemas ---

# Schema for authentication tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data (used during authentication)
class TokenData(BaseModel):
    email: Optional[str] = None

# --- Permission Schemas ---

# Schema for creating permissions (if needed in API)
class PermissionCreate(BaseModel):
    name: str  # Permission name like 'create', 'edit', etc.

# Schema for outputting permissions
class PermissionOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# --- UserPermission Schemas ---

# This schema can be used to link users with permissions
class UserPermissionOut(BaseModel):
    user_id: int
    permission_id: int

    class Config:
        orm_mode = True
