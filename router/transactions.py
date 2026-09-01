from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from database import get_db
from models import Transaction
from schemas import TransactionCreate, TransactionResponse, TransactionUpdate
from .auth import db_dependency, user_dependency
router = APIRouter()

@router.post("/create_transaction", response_model=TransactionResponse, status_code=201)

def create_transaction(transaction: TransactionCreate, user: user_dependency, db: db_dependency):

    new_transaction = Transaction(
        title= transaction.title,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        date=transaction.date,
        owner_id= user["id"]
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

@router.get("/transactions", response_model=list[TransactionResponse])

def get_transactions(user:user_dependency, db: db_dependency):

    transactions = db.query(Transaction).filter(Transaction.owner_id == user["id"]).all()

    return transactions

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)

def get_transaction(trasaction_id: int, user: user_dependency, db: db_dependency):
    trasaction = db.query(Transaction).filter(Transaction.id == trasaction_id, Transaction.owner_id == user["id"]).first()

    if trasaction is None:
        raise HTTPException(status_code=404, detail="Transaction not Found")

    return trasaction

@router.put("/transaction/{transaction_id}", response_model=TransactionResponse)

def update_transacation(transaction_id: int, transaction_data: TransactionUpdate, user: user_dependency, db: db_dependency):

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.owner_id == user["id"]).first()

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction Not Found")

    transaction.title = transaction_data.title
    transaction.amount = transaction_data.amount
    transaction.type = transaction_data.type
    transaction.category = transaction_data.category
    transaction.date = transaction_data.date

    db.commit()
    db.refresh(transaction)

    return transaction

@router.delete("/{transaction_id}", status_code=200)
def delete_transaction(transaction_id: int, user: user_dependency, db: db_dependency):

    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.owner_id == user["id"]).first()

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction Not Found")

    db.delete(transaction)
    db.commit()

    return{"message":"transaction delete successfully"}

@router.get("/transaction/filter", response_model=list[TransactionResponse])
def filter_transaction(user: user_dependency, db: db_dependency, type:str | None=None, category:str | None = None, min_amount: float | None = None, mx_amount: float | None = None):

    query = db.query(Transaction).filter(Transaction.owner_id == user["id"])

    if type is not None:
        query = query.filter(Transaction.type == type)
    if category is not None:
            query = query.filter(Transaction.category == category)
    if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
    if mx_amount is not None:
            query = query.filter(Transaction.amount <= mx_amount)

    return query.all()

