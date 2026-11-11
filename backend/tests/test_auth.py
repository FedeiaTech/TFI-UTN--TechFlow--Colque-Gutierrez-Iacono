import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.database.session import get_engine
from app.main import app
from app.models import Usuario
from app.core.security import get_password_hash

client = TestClient(app)

pytestmark = pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="DATABASE_URL not set")


@pytest.fixture
def usuario_test():
    """Crea un usuario real en Supabase para probar el ciclo de login."""
    password_plano = "secreto123"
    # Dominio .com para que email-validator lo acepte sin rechazar TLDs locales
    email_test = f"usuario_{os.urandom(4).hex()}@test.com"
    hash_pwd = get_password_hash(password_plano)

    with Session(get_engine()) as session:
        result = session.execute(
            insert(Usuario)
            .values(
                nombre="Usuario Auth Test",
                email=email_test,
                password_hash=hash_pwd,
            )
            .returning(Usuario.id)
        )
        user_id = result.scalar_one()
        session.commit()

    return {"id": user_id, "email": email_test, "password": password_plano}


def test_login_exitoso(usuario_test):
    response = client.post(
        "/auth/login",
        json={
            "email": usuario_test["email"],
            "password": usuario_test["password"],
        },
    )
    assert response.status_code == 200, f"Error en login exitoso: {response.text}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_credenciales_invalidas(usuario_test):
    response = client.post(
        "/auth/login",
        json={
            "email": usuario_test["email"],
            "password": "password_incorrecto",
        },
    )
    assert response.status_code == 401, f"Error en credenciales invalidas: {response.text}"


def test_acceso_ruta_protegida_con_token(usuario_test):
    # 1. Login
    login_res = client.post(
        "/auth/login",
        json={
            "email": usuario_test["email"],
            "password": usuario_test["password"],
        },
    )
    assert login_res.status_code == 200, f"Login fallo: {login_res.text}"
    token = login_res.json()["access_token"]

    # 2. Acceso a /auth/me con Authorization header Bearer
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == usuario_test["email"]


def test_acceso_ruta_protegida_sin_token_falla():
    res = client.get("/auth/me")
    assert res.status_code in (401, 403)