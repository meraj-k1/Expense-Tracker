from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User,Transaction
from schemas import UserCreate, UserResponse, LoginRequest,TokenResponse
from typing import Annotated
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

SECRET_KEY="7f4bc510e90bca49b654d44934eba83412bc1070d20fb33be71c6da1b0bf9e39"
ALGORITHM= "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password:str, hash_password:str):
    return pwd_context.verify(password, hash_password)

def create_access_token(username:str, user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    encode = {"sub":username, "id": user_id, "exp":expire}

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        return {"username": username, "id":user_id}

    except JWTError:
        raise HTTPException(status_code= 401, detail="Could not validate credentials")

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/register/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db:db_dependency):

    new_user = User(
        username= user.username,
        email = user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login', response_model=TokenResponse)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency):

    user = db.query(User).filter(User.username == form_data.username).first()
    
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(
        username=user.username, 
        user_id=user.id
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }