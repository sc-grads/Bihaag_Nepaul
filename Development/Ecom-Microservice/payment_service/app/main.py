# payment_service/main.py
from fastapi import Cookie, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import httpx
from fastapi.responses import JSONResponse
import paypalrestsdk
from datetime import datetime
import json
from . import models, schemas
from .database import SessionLocal, engine

# Initialize database
models.Base.metadata.create_all(bind=engine)

# Initialize PayPal
paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": "AVYZzxOit_f7vRlQwXav5iXZc-PuTS7atIyXBMP1wdsX9ifFwhTKrQBjU7jOQ-Zat7NwXWsizkNYIuuS",
    "client_secret": "EI9_c7T6lssSHu6t6qJafddPr6KPbKuE2vGyh3xUpmWVV9QbLvJwiRnwufBIVvr8RYWbDYnRMRn5n7ew"
})

app = FastAPI()

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

@app.post("/payment/create", response_model=schemas.PaymentResponse)
async def create_payment(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Fetch cart items
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://cart_service:8000/cart",
            cookies={"user_id": str(user_id)}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Could not fetch cart")
        
        cart_data = response.json()
        
    if not cart_data["items"]:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Create PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(cart_data["total"]),
                "currency": "USD"
            },
            "description": f"Purchase from Your E-commerce Store"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8080/payment/success",
            "cancel_url": "http://localhost:8080/payment/cancel"
        }
    })

    if payment.create():
        # Store payment information in database
        db_payment = models.Payment(
            user_id=user_id,
            payment_id=payment.id,
            amount=cart_data["total"],
            status="created"
        )
        db.add(db_payment)
        db.commit()

        # Get approval URL
        approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
        
        return {"payment_id": payment.id, "approval_url": approval_url}
    else:
        raise HTTPException(status_code=400, detail=payment.error)

@app.get("/payment/execute/{payment_id}")
async def execute_payment(
    payment_id: str,
    payer_id: str,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"payer_id": payer_id}):
        # Update payment status in database
        db_payment = db.query(models.Payment).filter(
            models.Payment.payment_id == payment_id,
            models.Payment.user_id == user_id
        ).first()
        
        if db_payment:
            db_payment.status = "completed"
            db_payment.completed_at = datetime.utcnow()
            db.commit()

            # Create order record
            db_order = models.Order(
                user_id=user_id,
                payment_id=payment_id,
                total_amount=db_payment.amount,
                status="confirmed"
            )
            db.add(db_order)
            db.commit()

            # Clear the cart
            async with httpx.AsyncClient() as client:
                cart_items = await client.get(
                    "http://cart_service:8000/cart",
                    cookies={"user_id": str(user_id)}
                )
                for item in cart_items.json()["items"]:
                    await client.delete(
                        f"http://cart_service:8000/cart/{item['id']}",
                        cookies={"user_id": str(user_id)}
                    )

            return {"status": "success", "order_id": db_order.id}
        
    raise HTTPException(status_code=400, detail="Payment execution failed")

@app.get("/payment/status/{payment_id}")
async def get_payment_status(
    payment_id: str,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    payment = db.query(models.Payment).filter(
        models.Payment.payment_id == payment_id,
        models.Payment.user_id == user_id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    return {"status": payment.status}



