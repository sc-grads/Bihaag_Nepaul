import json
import logging
from fastapi import FastAPI, HTTPException, Depends, Cookie, Response, logger
from sqlalchemy.orm import Session
from typing import Optional
import httpx
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas
from .database import SessionLocal, engine

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Add your frontend URL for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user_id(user_id: Optional[str] = Cookie(None)) -> int:
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return int(user_id)

@app.post("/cart/add", response_model=schemas.CartItemResponse)
async def add_to_cart(
    cart_item: schemas.CartItemCreate,
    response: Response,  # FastAPI Response object
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    logger.debug(f"User {user_id} is attempting to add product ID {cart_item.product_id} to their cart.")
    
    try:
        async with httpx.AsyncClient() as client:
            product_response = await client.get(f"http://product_service:8000/products/{cart_item.product_id}")
            product_response.raise_for_status()
            product_data = product_response.json()
            logger.info(f"Successfully retrieved product data for ID {cart_item.product_id}: {product_data}")
    except httpx.HTTPStatusError:
        logger.error(f"Product not found: ID {cart_item.product_id}")
        raise HTTPException(status_code=404, detail="Product not found")
    except httpx.RequestError as e:
        logger.error(f"Product service is unavailable: {str(e)}")
        raise HTTPException(status_code=500, detail="Product service is unavailable")

    # Check if item already in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == cart_item.product_id
    ).first()

    if existing_item:
        logger.debug(f"Item already in cart. Updating quantity for product ID {cart_item.product_id}.")
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
    else:
        # Create new cart item
        db_cart_item = models.CartItem(
            user_id=user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=product_data["price"]
        )
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)
        logger.info(f"Added new cart item for user {user_id}: {db_cart_item}")

    # Retrieve updated cart data from the database
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    
    # Create a summary that includes total items and a list of item IDs
    total_items = sum(item.quantity for item in cart_items)
    item_ids = [item.product_id for item in cart_items]  # List of product IDs in the cart

    # Store a summary of the cart (total items and item IDs) in a cookie
    response.set_cookie(
        key="cart_summary",
        value=json.dumps({"total_items": total_items, "item_ids": item_ids}),  # Use json.dumps
        httponly=False,  # Can be accessed by JavaScript (optional)
        max_age=3600,  # Expire after an hour
        secure=True,  # Set to True in production (HTTPS)
        samesite="Lax"
    )

    logger.debug(f"Cart summary updated for user {user_id}: Total items {total_items}, Item IDs {item_ids}")

    return db_cart_item


@app.get("/cart", response_model=schemas.CartResponse)
def get_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    total = sum(item.price * item.quantity for item in cart_items)
    return {"items": cart_items, "total": total}

@app.delete("/cart/{item_id}")
def remove_from_cart(
    item_id: int,
    response: Response,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Find the cart item to remove
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Remove the item from the cart
    db.delete(cart_item)
    db.commit()
    
    # After removing the item, retrieve the updated cart
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

    # Create an updated summary that includes total items and a list of item IDs
    total_items = sum(item.quantity for item in cart_items)
    item_ids = [item.product_id for item in cart_items]  # List of product IDs in the cart
    
    # Update the cart summary cookie
    response.set_cookie(
        key="cart_summary",
        value=json.dumps({"total_items": total_items, "item_ids": item_ids}),
        httponly=False,  # Can be accessed by JavaScript (optional)
        max_age=3600,  # Expire after an hour
        secure=True,  # Set to True in production (HTTPS)
        samesite="Lax"
    )

    logger.debug(f"Cart summary updated after removal for user {user_id}: Total items {total_items}, Item IDs {item_ids}")
    
    return {"message": "Item removed from cart", "cart_summary": {"total_items": total_items, "item_ids": item_ids}}

