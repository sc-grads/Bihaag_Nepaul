# payment_service/main.py
from fastapi import Cookie, FastAPI, HTTPException, Depends, Response, logger
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import httpx
from fastapi.responses import JSONResponse, RedirectResponse
import paypalrestsdk
from datetime import datetime
import json
from . import models, schemas
from .database import SessionLocal, engine
templates = Jinja2Templates(directory="templates")
# Initialize database
import urllib.parse
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
            db.refresh(db_order)  # Refresh to get the new order ID
            
            # Fetch cart items to create order items
            async with httpx.AsyncClient() as client:
                cart_items_response = await client.get(
                    "http://cart_service:8000/cart",
                    cookies={"user_id": str(user_id)}
                )
                cart_items = cart_items_response.json()["items"]
                
                # Add order items to the database
                for item in cart_items:
                    order_item = models.OrderItem(
                        order_id=db_order.id,
                        product_id=item['product_id'],
                        quantity=item['quantity'],
                        price=item['price']  # Assume you have the price in the cart
                    )
                    db.add(order_item)
                db.commit()  # Commit all order items

            # Clear the cart
            async with httpx.AsyncClient() as client:
                for item in cart_items:
                    await client.delete(
                        f"http://cart_service:8000/cart/{item['id']}",
                        cookies={"user_id": str(user_id)}
                    )

            return {
                "status": "success", 
                "order_id": db_order.id, 
                "payment_id": payment_id, 
                "total_amount": db_payment.amount
            }
        
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


@app.get("/payment/success")
async def payment_success(
    paymentId: str,
    token: str,
    PayerID: str,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Execute the payment and retrieve order information
    order_data = await execute_payment(payment_id=paymentId, payer_id=PayerID, user_id=user_id, db=db)
    
    # Fetch cart data and product details
    async with httpx.AsyncClient() as client:
        # Get cart items
        cart_response = await client.get(
            "http://cart_service:8000/cart",
            cookies={"user_id": str(user_id)}
        )
        cart_data = cart_response.json()
        
        # For each cart item, fetch product details
        cart_items = []
        for item in cart_data["items"]:
            try:
                product_response = await client.get(
                    f"http://product_service:8000/products/{item['product_id']}"
                )
                if product_response.status_code == 200:
                    product = product_response.json()
                    cart_items.append({
                        "name": product["name"],
                        "quantity": item["quantity"],
                        "price": item["price"]
                    })
            except Exception as e:
                logger.error(f"Error fetching product details: {str(e)}")
                # Fall back to basic information if product details unavailable
                cart_items.append({
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "price": item["price"]
                })

    # URL-encode the cart data
    cart_items_encoded = urllib.parse.quote(json.dumps(cart_items))

    # Construct the redirect URL with all parameters
    redirect_url = (
        f"/payment_success.html"
        f"?order_id={order_data['order_id']}"
        f"&payment_id={paymentId}"
        f"&total_amount={order_data['total_amount']}"
        f"&cart_items={cart_items_encoded}"
    )

    return RedirectResponse(url=redirect_url)

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
    

@app.get("/orders/", response_model=List[schemas.OrderResponse])
async def get_order_history(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders