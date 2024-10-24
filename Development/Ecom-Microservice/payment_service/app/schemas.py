from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    amount: float

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(BaseModel):
    payment_id: str
    approval_url: str

class PaymentStatus(BaseModel):
    status: str
    payment_id: str
    amount: float
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    payment_id: str
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
