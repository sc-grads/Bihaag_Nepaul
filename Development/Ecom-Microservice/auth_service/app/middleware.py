from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Permission, UserPermission, ServiceEnum
import functools

def check_permissions(action: str, service: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: Request, db: Session = Depends(get_db)):
            # Ensure user is properly set in request context
            if not hasattr(request, 'user') or request.user is None:
                raise HTTPException(status_code=401, detail="User not authenticated")

            user_id = request.user.id  # Assuming user object is attached to the request
            method = request.method.lower()

            # Get service from the ServiceEnum
            try:
                service_enum = ServiceEnum[service.upper()]
            except KeyError:
                raise HTTPException(status_code=400, detail="Invalid service specified")

            # Get user's permissions for this service
            user_permissions = (
                db.query(UserPermission)
                .join(Permission)
                .filter(
                    UserPermission.user_id == user_id,
                    Permission.service == service_enum
                )
                .all()
            )
            
            permissions = {p.permission.name for p in user_permissions}

            # Define required permission for each method
            required_permissions = {
                "get": "view",
                "post": "create",
                "put": "edit",
                "delete": "delete"
            }

            required_perm = required_permissions.get(method)
            if required_perm is None:
                raise HTTPException(status_code=405, detail="Method not allowed")

            # Check if the user has the required permission
            if required_perm not in permissions:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Not enough permissions for {method} operation in {service} service"
                )

            # Proceed to call the original function
            return await func(request, db)
        return wrapper
    return decorator
