"""Smoke tests for health endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ONLINE"
    assert data["service"] == "GoodLife Gateway Fabric"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "HEALTHY"
    assert "version" in data
