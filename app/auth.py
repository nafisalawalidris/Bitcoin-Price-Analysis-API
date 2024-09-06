from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from app.config import settings
from app.database import get_db
from sqlalchemy.orm import Session

# Initialize the router
router = APIRouter()

# OAuth2 scheme for JWT Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define a model for the token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Define a model for user credentials
class TokenData(BaseModel):
    username: str

# JWT secret key and algorithm
SECRET_KEY = settings.api_key  # Ensure this is set in your .env file
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time in minutes

# Function to create a new JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

# Route to generate a new token (mock example, adjust based on your actual user validation)
@router.post("/token", response_model=Token)
async def login(form_data: dict, db: Session = Depends(get_db)):
    # Mock user authentication, replace with actual user validation logic
    username = form_data.get("username")
    password = form_data.get("password")
    if username != "testuser" or password != "testpassword":  # Mock validation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Example protected route
@router.get("/users/me", response_model=TokenData)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    return current_user
