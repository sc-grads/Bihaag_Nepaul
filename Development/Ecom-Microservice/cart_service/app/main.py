from fastapi import FastAPI, HTTPException, Depends, Cookie
from sqlalchemy.orm import Session
from typing import Optional
import httpx
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas
from .database import SessionLocal, engine

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
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://product_service:8000/products/{cart_item.product_id}")
            response.raise_for_status()
            product_data = response.json()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Product not found")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Product service is unavailable")

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

@app.get("/cart", response_model=schemas.CartResponse)
def get_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
    total = sum(item.price * item.quantity for item in cart_items)
    return {"items": cart_items, "total": total}

@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.user_id == user_id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}
