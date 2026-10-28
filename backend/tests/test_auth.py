import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_exitoso():
    response = client.post("/auth/login", json={
        "email": "admin@techflow.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_credenciales_invalidas():
    response = client.post("/auth/login", json={
        "email": "admin@techflow.com",
        "password": "password_incorrecta"
    })
    assert response.status_code == 401
    assert "Credenciales incorrectas" in response.json()["detail"]


def test_acceso_ruta_protegida_con_token():
    # 1. Obtener token
    login_res = client.post("/auth/login", json={
        "email": "admin@techflow.com",
        "password": "admin123"
    })
    token = login_res.json()["access_token"]

    # 2. Consultar /auth/me con el header Bearer
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/auth/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["usuario"] == "admin@techflow.com"


def test_acceso_ruta_protegida_sin_token_falla():
    res = client.get("/auth/me")
    assert res.status_code == 403 or res.status_code == 401