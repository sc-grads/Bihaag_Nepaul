#product_service/app/auth_middleware.py

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from enum import Enum
from typing import Optional
from auth_service.app import models
from auth_service.app.auth import verify_token_and_permissions  # Import the token verification function
import logging

logging.basicConfig(level=logging.INFO)

SECRET_KEY = "e3aac17d09746a3effe0dd1b414b9e3e8d64b30a53d2e27b1b5f69e4ed35d2e0"
ALGORITHM = "HS256"

class ServiceEnum(str, Enum):
    CART = "cart"
    PRODUCT = "product"  # Changed to lowercase to be consistent
    SELLER = "seller"
    PAYMENT = "payment"
    AUTH = "auth"

async def get_token_from_header(request: Request) -> Optional[str]:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="No authorization header found"
        )
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )
        return token
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

def verify_permission(action: str, service: ServiceEnum):
    async def permission_dependency(
        request: Request,
        token: str = Depends(get_token_from_header)
    ):
        # Verify the token and get user info
        required_roles = ["user", "admin"]  # Define roles required for access
        payload = await verify_token_and_permissions(token, required_roles)
        
        user_email = payload.get("email")
        user_role = payload.get("role")

        if not user_email:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        logging.info(f"User Email: {user_email}, Role: {user_role}")

        # Admin users bypass permission checks
        if user_role == "admin":
            return True

        # Connect to auth database to check permissions
        from .database import SessionLocal
        db: Session = SessionLocal()
        try:
            # Get the user and their permissions
            user = db.query(models.User).filter(models.User.email == user_email).first()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="User not found"
                )

            logging.info(f"Permissions for user {user_email}: {user.permissions}")

            # Check if user has the required permission for this service
            has_permission = False
            for user_permission in user.permissions:
                if (user_permission.permission.service == service and 
                    user_permission.permission.name == action):
                    has_permission = True
                    break

            if not has_permission:
                raise HTTPException(
                    status_code=403,
                    detail=f"Not enough permissions for {action} operation in {service.value} service"
                )

            return True
        finally:
            db.close()

    return permission_dependency
