from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User
from fastapi import status

client = TestClient(app)

def create_test_user():
    db = SessionLocal()

    username = "testuser"

    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        db.close()
        return existing_user

    response = client.post("/register/",json={
        "username":username,
        "email":"testuser@gmail.com",
        "password":"1234"
    })

    db.close()

    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

def get_token():
    create_test_user()

    response= client.post("/login", data={
        "username": "testuser",
        "password": "1234"
    })

    assert response.status_code == status.HTTP_200_OK

    return response.json()["access_token"]

def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

def test_create_transaction():
    token = get_token()

    response = client.post("/create_transaction/", json={
        "title": "Lunch",
        "amount": 200,
        "type": "expense",
        "category": "Food",
        "date": "2026-08-31"
    },
    headers={
        "Authorization":f"Bearer {token}"
    })

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["title"] == "Lunch"
    assert data["amount"] == 200

def test_delete_transaction():
    token = get_token()

    response = client.post("/create_transaction/", json={
        "title": "Dinner",
        "amount": 400,
        "type": "expense",
        "category": "Food",
        "date": "2026-08-31"
    },
    headers={
        "Authorization":f"Bearer {token}"
    })

    assert response.status_code == status.HTTP_201_CREATED
    transaction_id = response.json()["id"]

    response = client.delete(f"/{transaction_id}/",headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == status.HTTP_200_OK

def test_get_transaction():
    token = get_token()

    response = client.get("/transactions/",
    headers={
        "Authorization":f"Bearer {token}"
    })

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.json(), list)

def test_transaction_without_token():

    response = client.get("/transactions")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_filter_transaction():

    token = get_token()

    response = client.get(
        "/transaction/filter",
        params={
            "category": "Food"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.json(), list)

def test_update_transaction():
    token = get_token()

    response = client.post("/create_transaction/", json={
        "title": "Dinner",
        "amount": 400,
        "type": "expense",
        "category": "Food",
        "date": "2026-08-31"
    },
    headers={
        "Authorization":f"Bearer {token}"
    })

    assert response.status_code == status.HTTP_201_CREATED
    transaction_id = response.json()["id"]

    response = client.put(f"/transaction/{transaction_id}/",json={
        "title": "Dinner",
        "amount": 400,
        "type": "expense",
        "category": "Food",
        "date": "2026-08-31"
        
    },headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == status.HTTP_200_OK