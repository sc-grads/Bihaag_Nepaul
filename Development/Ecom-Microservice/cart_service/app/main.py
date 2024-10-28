import json
import logging
from fastapi import FastAPI, HTTPException, Depends, Cookie, Response
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

async def get_product_details(product_id: int, client: httpx.AsyncClient) -> dict:
    """Helper function to get product details including name."""
    try:
        response = await client.get(f"http://product_service:8000/products/{product_id}")
        response.raise_for_status()
        product_data = response.json()
        logger.debug(f"Product service response for ID {product_id}: {product_data}")
        return {
            "name": product_data.get("name", f"Product {product_id}"),
            "price": product_data.get("price", 0)
        }
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch product {product_id}: {str(e)}")
        return {"name": f"Product {product_id}", "price": 0}

@app.post("/cart/add", response_model=schemas.CartItemResponse)
async def add_to_cart(
    cart_item: schemas.CartItemCreate,
    response: Response,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    logger.debug(f"User {user_id} is attempting to add product ID {cart_item.product_id} to their cart.")
    
    # Get product details for the item being added
    try:
        async with httpx.AsyncClient() as client:
            product_info = await get_product_details(cart_item.product_id, client)
            logger.info(f"Successfully retrieved product data for ID {cart_item.product_id}: {product_info}")
    except Exception as e:
        logger.error(f"Error fetching product details: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching product details")

    # Check if item already in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == cart_item.product_id
    ).first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
    else:
        db_cart_item = models.CartItem(
            user_id=user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=product_info["price"],
            product_name=product_info["name"]  # Store the product name
        )
        db.add(db_cart_item)
        db.commit()
        db.refresh(db_cart_item)

    # Get all cart items and their details
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    
    # Use stored product details from database
    cart_details = []
    total_amount = 0
    for item in cart_items:
        cart_details.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "name": item.product_name,  # Use stored name
            "price": item.price
        })
        total_amount += item.quantity * item.price

    total_items = sum(item.quantity for item in cart_items)

    # Create enhanced cart summary
    cart_summary = {
        "total_items": total_items,
        "total_amount": total_amount,
        "cart_details": cart_details
    }
    
    logger.debug(f"Setting cart summary cookie: {cart_summary}")
    
    # Set the cookie with the enhanced cart information
    response.set_cookie(
        key="cart_summary",
        value=json.dumps(cart_summary),
        httponly=False,
        max_age=3600,
        secure=True,
        samesite="Lax"
    )

    return db_cart_item

@app.get("/cart", response_model=schemas.CartResponse)
def get_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    total = sum(item.price * item.quantity for item in cart_items)
    return {"items": cart_items, "total": total}

@app.post("/cart/update", response_model=schemas.CartItemResponse)
async def update_cart_item(
    cart_item: schemas.CartItemCreate,
    response: Response,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    logger.debug(f"User {user_id} is attempting to update product ID {cart_item.product_id} in their cart.")

    # Check if item exists in the cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == cart_item.product_id
    ).first()

    if not existing_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    existing_item.quantity = cart_item.quantity
    db.commit()
    db.refresh(existing_item)
    logger.info(f"Updated cart item for user {user_id}: {existing_item}")

    # Get all cart items
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

    # Fetch product details for all items in cart
    cart_details = []
    async with httpx.AsyncClient() as client:
        for item in cart_items:
            product_info = await get_product_details(item.product_id, client)
            cart_details.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "name": product_info["name"]
            })

    total_items = sum(item.quantity for item in cart_items)

    # Update the cart summary cookie with detailed cart information
    response.set_cookie(
        key="cart_summary",
        value=json.dumps({
            "total_items": total_items,
            "cart_details": cart_details
        }),
        httponly=False,
        max_age=3600,
        secure=True,
        samesite="Lax"
    )

    return existing_item

@app.delete("/cart/{item_id}")
async def remove_from_cart(
    item_id: int,
    response: Response,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    logger.debug(f"User {user_id} is attempting to remove item ID {item_id} from their cart.")
    
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    
    # Get updated cart items
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

    # Fetch product details for remaining items
    cart_details = []
    async with httpx.AsyncClient() as client:
        for item in cart_items:
            product_info = await get_product_details(item.product_id, client)
            cart_details.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "name": product_info["name"]
            })
            logger.debug(f"Added to cart details: {cart_details[-1]}")

    total_items = sum(item.quantity for item in cart_items)
    
    cart_summary = {
        "total_items": total_items,
        "cart_details": cart_details
    }
    
    logger.debug(f"Setting cart summary cookie: {cart_summary}")
    
    response.set_cookie(
        key="cart_summary",
        value=json.dumps(cart_summary),
        httponly=False,
        max_age=3600,
        secure=True,
        samesite="Lax"
    )
    
    return {"message": "Item removed from cart", "cart_summary": cart_summary}