from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, schemas, database
from typing import List
import os
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func


app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="uploaded_images")
# Ensure the database tables are created
models.Base.metadata.create_all(bind=database.engine)

# Define the upload directory
UPLOAD_DIRECTORY = "uploaded_images"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Route to serve the product creation form
@app.get("/products/new", response_class=HTMLResponse)
async def new_product_form(request: Request):
    return templates.TemplateResponse("product_form.html", {"request": request})

# Route to create a new product
@app.post("/products/", response_model=schemas.Product)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    seller_id: int = Form(...),
    brand: str = Form(...),
    quantity: int = Form(1),  # New field for quantity with default of 1
    image: UploadFile = File(None),
    db: Session = Depends(database.get_db)
):
    image_url = None
    if image and image.filename:
        filename = f"{name}_{image.filename}"
        filepath = os.path.join(UPLOAD_DIRECTORY, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await image.read())
        image_url = f"/uploaded_images/{filename}"

    db_product = models.Product(
        name=name, 
        description=description, 
        price=price, 
        image_url=image_url, 
        seller_id=seller_id,
        brand=brand,
        quantity=quantity  # Handle quantity here
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Route to read all products
@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

# Route to read a single product by ID
@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Route to serve the edit form for a product
@app.get("/products/{product_id}/edit", response_class=HTMLResponse)
async def edit_product_form(product_id: int, request: Request, db: Session = Depends(database.get_db)):
    print(f"Editing product with ID: {product_id}")  # Debug line
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("product_edit.html", {"request": request, "product": db_product})



# Route to update a product
@app.post("/products/{product_id}/edit", response_model=schemas.Product)
async def update_product(
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),  # New field for quantity update
    image: UploadFile = File(None),
    db: Session = Depends(database.get_db)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.name = name
    db_product.description = description
    db_product.price = price
    db_product.quantity = quantity  # Update quantity here
    
    if image and image.filename:
        filename = f"{name}_{image.filename}"
        filepath = os.path.join(UPLOAD_DIRECTORY, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await image.read())
        db_product.image_url = f"/uploaded_images/{filename}"
    
    db.commit()
    db.refresh(db_product)
    return db_product


# Route to delete a product
@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product

# Route to search for products
@app.get("/products/search/", response_model=List[schemas.Product])
def search_products(query: str, db: Session = Depends(database.get_db)):
    products = db.query(models.Product).filter(
        (models.Product.name.ilike(f"%{query}%")) | 
        (models.Product.description.ilike(f"%{query}%"))
    ).all()
    return products

# Route to get all categories
@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(database.get_db)):
    categories = db.query(models.Category).all()
    return categories

# Route to get products by category
@app.get("/products/category/{category_id}", response_model=List[schemas.Product])
def read_products_by_category(category_id: int, db: Session = Depends(database.get_db)):
    products = db.query(models.Product).filter(models.Product.category_id == category_id).all()
    return products

@app.get("/products/brand/{brand}", response_model=List[schemas.Product])
def read_products_by_brand(brand: str, db: Session = Depends(database.get_db)):
    products = db.query(models.Product).filter(models.Product.brand == brand).all()
    return products

@app.get("/products/year/{year}", response_model=List[schemas.Product])
def read_products_by_year(year: int, db: Session = Depends(database.get_db)):
    products = db.query(models.Product).filter(func.extract('year', models.Product.time_added) == year).all()
    return products

