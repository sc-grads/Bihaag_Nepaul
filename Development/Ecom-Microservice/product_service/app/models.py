from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    seller_id = Column(Integer)
    brand = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))  # Foreign key to Category
    time_added = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Integer, default=1)  # New quantity field
