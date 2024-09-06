from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
import jwt
import datetime
from app.database import get_db
from app.models.user import User  # Ensure you have a User model for authentication
from app.utils import verify_password, create_password_hash, create_jwt_token

# Set up the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create the router instance
auth = APIRouter()

@auth.get("/login")
def login():
    return {"message": "Login endpoint"}

# Models
class UserInDB(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

# Dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])  # Replace "SECRET_KEY" with your secret key
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(user: UserInDB, db: Session = Depends(get_db)):
    hashed_password = create_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.get("/users/me")
def read_users_me(current_user: TokenData = Depends(get_current_user)):
    return {"username": current_user.username}

# Utility functions (utils.py)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Implement password verification logic here
    return hashed_password == create_password_hash(plain_password)

def create_password_hash(password: str) -> str:
    # Implement password hashing logic here
    return password  # Replace this with actual hashing logic

def create_jwt_token(data: dict) -> str:
    # Implement JWT token creation logic here
    return jwt.encode(data, "SECRET_KEY", algorithm="HS256")  # Replace "SECRET_KEY" with your secret key

