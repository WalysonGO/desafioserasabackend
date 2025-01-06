import pytest
from fastapi.testclient import TestClient
from app.main import app

import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

def test_hello_world(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World! 👋 Desafio Técnico SERASA."}

def test_register_user_invalid_data(test_client):
    response = test_client.post("/users/register", json={
       "username": "teste",
       "pass": "test"
    })
    assert response.status_code == 422

def test_login_user_success(test_client):
    response = test_client.post("/users/login", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_invalid_credentials(test_client):
    response = test_client.post("/users/login", json={
        "email": "invalid@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 400

def test_add_debt(test_client):
    login_response = test_client.post("/users/login", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = test_client.post("/debts/", json={
        "title": "Cartão de Crédito",
        "amount": 1000.00,
        "due_date": "2024-12-31",
        "status": "Pendente"
    }, headers=headers)

    assert response.status_code == 200

def test_add_debt_without_auth(test_client):
    response = test_client.post("/debts/", json={
        "title": "Cartão de Crédito",
        "amount": 1000.00,
        "due_date": "2024-12-31",
        "status": "Pendente"
    })
    
    assert response.status_code == 401

def test_financial_summary(test_client):
    login_response = test_client.post("/users/login", json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = test_client.get("/debts/summary", headers=headers)
    
    assert response.status_code == 200
