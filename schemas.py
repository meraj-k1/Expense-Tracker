from datetime import datetime, date
from pydantic import BaseModel, Field,EmailStr, field_validator
from typing import Optional, Literal

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    # id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True 

class LoginRequest(BaseModel):
    username: str
    # email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TransactionCreate(BaseModel):
    title: str
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    type: Literal["income", "expense"]
    category: str
    date: date

class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str
    date: date
    

    class Config:
        from_attributes = True

class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0, description="Amount must be greater than zero")
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    date: date 
