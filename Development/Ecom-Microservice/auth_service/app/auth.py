from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, database
from fastapi import APIRouter, Depends, Request

from fastapi.responses import JSONResponse, RedirectResponse
import os

SECRET_KEY = "e3aac17d09746a3effe0dd1b414b9e3e8d64b30a53d2e27b1b5f69e4ed35d2e0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    """Verifies a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hashes the password."""
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    """Authenticates a user based on their email and password."""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"role": data.get("role", "user")})  # Include role in token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token_and_permissions(token: str, required_roles: list[str]) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        if role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
            
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Retrieves the current user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """Ensures the current user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_user_role(current_user: models.User = Depends(get_current_user)):
    """Retrieves the role of the current user."""
    return current_user.role

def get_user_role(user: models.User) -> schemas.RoleEnum:
    """Retrieves the role of a user."""
    return user.role

def get_admin_user(current_user: models.User = Depends(get_current_user)):
    """Ensures the user has an admin role."""
    if current_user.role != schemas.RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")
    return current_user

def assign_permissions(user: models.User, db_session: Session):
    if user.role == models.UserRole.ADMIN:
        # Assign all permissions for admin
        permissions = db_session.query(models.Permission).all()
    else:
        # Map regular user permissions
        service_permissions = {
            models.ServiceEnum.CART: ["create", "view", "edit", "delete"],
            models.ServiceEnum.PRODUCT: ["view"],
            models.ServiceEnum.PAYMENT: ["create", "view", "edit", "delete"]
        }
        
        permissions = []
        for service, perms in service_permissions.items():
            service_perms = db_session.query(models.Permission).filter(
                models.Permission.service == service,
                models.Permission.name.in_(perms)
            ).all()
            permissions.extend(service_perms)

    # Assign permissions to user
    for permission in permissions:
        user_permission = models.UserPermission(user_id=user.id, permission_id=permission.id)
        db_session.add(user_permission)
    
    db_session.commit()

