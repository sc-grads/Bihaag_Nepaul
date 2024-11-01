from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum

from .database import Base

class ServiceEnum(str, enum.Enum):
    CART = "cart"
    PRODUCT = "product"
    SELLER = "seller"
    PAYMENT = "payment"
    AUTH = "auth"

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)  # Remove unique constraint
    service = Column(Enum(ServiceEnum), nullable=False)

    # Make the combination of name and service unique
    __table_args__ = (
        UniqueConstraint('name', 'service', name='unique_permission_per_service'),
    )
    
    users = relationship("UserPermission", back_populates="permission")

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    permissions = relationship("UserPermission", back_populates="user")

class UserPermission(Base):
    __tablename__ = "user_permissions"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)

    user = relationship("User", back_populates="permissions")
    permission = relationship("Permission", back_populates="users")
