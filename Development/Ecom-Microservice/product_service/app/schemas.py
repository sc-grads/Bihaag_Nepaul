from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------- Product Schemas ----------

class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    image_url: Optional[str] = None
    seller_id: int
    brand: str
    category_id: Optional[int] = None
    time_added: Optional[datetime] = None
    quantity: Optional[int] = 1
    is_bestseller: bool = False
    is_featured: bool = False  # Add the quantity field with default value

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image_url: Optional[str] = None
    brand: Optional[str] = None
    quantity: Optional[int] = None  # Allow updating quantity in ProductUpdate

# ---------- Category Schemas ----------

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2
