from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
from typing import List

router = APIRouter()

@router.post("/sellers/", response_model=schemas.Seller)
def create_seller(seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    db_seller = models.Seller(**seller.dict())
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

@router.get("/sellers/", response_model=List[schemas.Seller])
def read_sellers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sellers = db.query(models.Seller).offset(skip).limit(limit).all()
    return sellers

@router.get("/sellers/{seller_id}", response_model=schemas.Seller)
def read_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return db_seller

@router.put("/sellers/{seller_id}", response_model=schemas.Seller)
def update_seller(seller_id: int, seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    db_seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    for key, value in seller.dict().items():
        setattr(db_seller, key, value)
    db.commit()
    db.refresh(db_seller)
    return db_seller

@router.delete("/sellers/{seller_id}", response_model=schemas.Seller)
def delete_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    db.delete(db_seller)
    db.commit()
    return db_seller