from enum import Enum
from typing import Dict, List

class Role(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    USER = "user"

class Permission(str, Enum):
    # Product permissions
    CREATE_PRODUCT = "create:product"
    READ_PRODUCT = "read:product"
    UPDATE_PRODUCT = "update:product"
    DELETE_PRODUCT = "delete:product"
    
    # Order permissions
    CREATE_ORDER = "create:order"
    READ_ORDER = "read:order"
    UPDATE_ORDER = "update:order"
    
    # User management permissions
    MANAGE_USERS = "manage:users"
    READ_USERS = "read:users"
    
    # Seller permissions
    MANAGE_INVENTORY = "manage:inventory"
    VIEW_SALES = "view:sales"

# Role-Permission mapping
ROLE_PERMISSIONS: Dict[Role, List[Permission]] = {
    Role.ADMIN: [
        Permission.CREATE_PRODUCT, Permission.READ_PRODUCT,
        Permission.UPDATE_PRODUCT, Permission.DELETE_PRODUCT,
        Permission.READ_ORDER, Permission.UPDATE_ORDER,
        Permission.MANAGE_USERS, Permission.READ_USERS,
        Permission.VIEW_SALES
    ],
    Role.SELLER: [
        Permission.CREATE_PRODUCT, Permission.READ_PRODUCT,
        Permission.UPDATE_PRODUCT, Permission.DELETE_PRODUCT,
        Permission.MANAGE_INVENTORY, Permission.VIEW_SALES
    ],
    Role.CUSTOMER: [
        Permission.READ_PRODUCT,
        Permission.CREATE_ORDER,
        Permission.READ_ORDER
    ]
}

# JWT Configuration
JWT_CONFIG = {
    "SECRET_KEY": "your-secret-key",
    "ALGORITHM": "HS256",
    "TOKEN_EXPIRE_MINUTES": 30
}