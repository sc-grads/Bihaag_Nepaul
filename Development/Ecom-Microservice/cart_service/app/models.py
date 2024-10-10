from sqlalchemy import Column, Integer, ForeignKey, Float
from .database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    quantity = Column(Integer, default=1)
    price = Column(Float)  # Store the price at the time of adding to cart