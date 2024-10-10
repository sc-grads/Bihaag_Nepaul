from pydantic import BaseModel, EmailStr

class SellerBase(BaseModel):
    username: str
    email: EmailStr

class SellerCreate(SellerBase):
    password: str

class Seller(SellerBase):
    id: int

    class Config:
        orm_mode = True