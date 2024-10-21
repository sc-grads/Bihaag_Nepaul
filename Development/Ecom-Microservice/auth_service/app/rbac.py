from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import os

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")  # Use environment variable
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_token_and_permissions(token: str, required_roles: List[str]) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        if role not in required_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
            
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def rbac_middleware(required_roles: List[str]):
    async def wrapper(token: str = Depends(oauth2_scheme)):
        return await verify_token_and_permissions(token, required_roles)
    return wrapper