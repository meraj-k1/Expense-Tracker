from fastapi import FastAPI
from database import engine, Base
from models import User, Transaction
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Literal
from router import auth, transactions
from router.auth import user_dependency

import models

app = FastAPI()
app.include_router(auth.router)
app.include_router(transactions.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def view():
    return{"message": "Expense Tracker"}

