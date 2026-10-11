import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.skipif(not os.environ.get("DATABASE_URL"), reason="DATABASE_URL not set")
def test_health_db_ok():
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_db_without_database_url_returns_503(monkeypatch):
    from app.core.config import Settings, get_settings
    from app.database import session

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setitem(Settings.model_config, "env_file", None)
    get_settings.cache_clear()
    session.get_engine.cache_clear()
    try:
        response = client.get("/health/db")
        assert response.status_code == 503
        assert "postgresql" not in response.text.lower()
        assert "password" not in response.text.lower()
    finally:
        get_settings.cache_clear()
        session.get_engine.cache_clear()


def test_health_db_connection_failure_does_not_leak_url(monkeypatch):
    from app.core.config import get_settings
    from app.database import session

    secret_url = "postgresql://user:s3cr3t@127.0.0.1:1/db"
    monkeypatch.setenv("DATABASE_URL", secret_url)
    get_settings.cache_clear()
    session.get_engine.cache_clear()
    try:
        response = client.get("/health/db")
        assert response.status_code == 503
        assert "s3cr3t" not in response.text
        assert "127.0.0.1" not in response.text
    finally:
        get_settings.cache_clear()
        session.get_engine.cache_clear()
