from fastapi import FastAPI
from .seller import router as seller_router
from . import models
from .database import engine


app = FastAPI()



models.Base.metadata.create_all(bind=engine)

app.include_router(seller_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Seller Service"}