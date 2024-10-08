from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import httpx

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cart/add", response_model=schemas.CartItemResponse)
async def add_to_cart(
    cart_item: schemas.CartItemCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    # Verify product exists and get its price
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://product_service:8000/products/{cart_item.product_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
        product_data = response.json()
    
    # Check if item already in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == cart_item.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
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
    return db_cart_item

@app.get("/cart/{user_id}", response_model=schemas.CartResponse)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    total = sum(item.price * item.quantity for item in cart_items)
    return {"items": cart_items, "total": total}

@app.delete("/cart/{user_id}/{item_id}")
def remove_from_cart(user_id: int, item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user_id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}