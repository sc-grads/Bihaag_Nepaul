from fastapi import FastAPI, Depends, HTTPException, Request, status, Form, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates setup
templates = Jinja2Templates(directory="templates")

# Ensure the database tables are created
models.Base.metadata.create_all(bind=database.engine)

@app.get("/auth/register")
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Updated /auth/register route to include user roles
@app.post("/auth/register", response_model=schemas.UserOut)
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: schemas.RoleEnum = Form(default=schemas.RoleEnum.USER),  # Include role with default
    db: Session = Depends(database.get_db)
):
    try:
        logger.debug(f"Attempting to register user: {username}, {email}, role: {role}")
        db_user = db.query(models.User).filter(models.User.email == email).first()
        if db_user:
            logger.warning(f"Email already registered: {email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = auth.get_password_hash(password)
        new_user = models.User(username=username, email=email, hashed_password=hashed_password, role=role)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"Successfully registered user: {username}, {email}, role: {role}")
        return new_user
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/auth/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Set cookie on successful login
    response.set_cookie(key="user_id", value=user.id, httponly=True)

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in: {user.username}, role: {user.role}")
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@app.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="user_id")
    return {"message": "Logout successful"}

@app.get("/user/{user_id}", response_model=schemas.UserOut)
async def get_user_profile(user_id: int):
    db = database.get_db()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/me", response_model=schemas.UserOut)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


