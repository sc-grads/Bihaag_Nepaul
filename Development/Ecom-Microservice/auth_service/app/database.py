from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from sqlalchemy.exc import IntegrityError
  # Import your Permission and ServiceEnum models

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_permissions(db_session: Session):
    from .models import Permission, ServiceEnum
    # Define permissions per service
    service_permissions = {
        ServiceEnum.CART: ["create", "view", "edit", "delete"],
        ServiceEnum.PRODUCT: ["create", "view", "edit", "delete"],
        ServiceEnum.SELLER: ["create", "view", "edit", "delete"],
        ServiceEnum.PAYMENT: ["create", "view", "edit", "delete"],
        ServiceEnum.AUTH: ["create", "view", "edit", "delete"]
    }
    
    admin_permissions = {
        ServiceEnum.CART: ["create", "view", "edit", "delete"],
        ServiceEnum.PRODUCT: ["create", "view", "edit", "delete"],
        ServiceEnum.SELLER: ["create", "view", "edit", "delete"],
        ServiceEnum.PAYMENT: ["create", "view", "edit", "delete"],
        ServiceEnum.AUTH: ["create", "view", "edit", "delete"]
    }

    # Create all permissions in the database
    for service, perms in service_permissions.items():
        for perm in perms:
            permission = Permission(name=perm, service=service)
            db_session.add(permission)
    
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        print("Permissions already exist")
