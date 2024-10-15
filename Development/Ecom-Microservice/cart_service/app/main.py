from fastapi import FastAPI, HTTPException, Depends, Cookie
from sqlalchemy.orm import Session
from typing import Optional
import httpx
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas
from .database import SessionLocal, engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the correct origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


app = FastAPI()

# Configure CORS to allow cross-origin requests

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to retrieve the current user's ID from the cookie
async def get_current_user_id(user_id: Optional[str] = Cookie(None)) -> int:
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(user_id)

# Route to add an item to the cart
@app.post("/cart/add", response_model=schemas.CartItemResponse)
async def add_to_cart(
    cart_item: schemas.CartItemCreate,
    user_id: int = Depends(get_current_user_id),  # Fetch user ID from the cookie
    db: Session = Depends(get_db)
):
    # Verify the product exists and get its price
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://product_service:8000/products/{cart_item.product_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
        product_data = response.json()
    
    # Check if the item is already in the cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == cart_item.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    # Create a new cart item if it doesn't exist
    db_cart_item = models.CartItem(
        user_id=user_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        price=product_data["price"]
    )
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

# Route to get the user's cart
@app.get("/cart", response_model=schemas.CartResponse)
async def get_cart(
    user_id: int = Depends(get_current_user_id),  # Fetch user ID from the cookie
    db: Session = Depends(get_db)
):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    total = sum(item.price * item.quantity for item in cart_items)
    return {"items": cart_items, "total": total}

# Route to remove an item from the cart
@app.delete("/cart/{item_id}")
async def remove_from_cart(
    item_id: int,
    user_id: int = Depends(get_current_user_id),  # Fetch user ID from the cookie
    db: Session = Depends(get_db)
):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user_id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

# Route to clear all items in the user's cart
@app.delete("/cart")
async def clear_cart(
    user_id: int = Depends(get_current_user_id),  # Fetch user ID from the cookie
    db: Session = Depends(get_db)
):
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()
    return {"message": "Cart cleared"}

# Route to get a summary of the cart
@app.get("/cart/summary", response_model=schemas.CartSummaryResponse)
async def get_cart_summary(
    user_id: int = Depends(get_current_user_id),  # Fetch user ID from the cookie
    db: Session = Depends(get_db)
):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    total_price = sum(item.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    return {"total_price": total_price, "total_items": total_items}



@app.get("/cart", response_model=schemas.CartResponse)
async def get_cart(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching cart for user {user_id}")
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    total = sum(item.price * item.quantity for item in cart_items)
    logger.info(f"Cart fetched: {len(cart_items)} items, total ${total}")
    return {"items": cart_items, "total": total}