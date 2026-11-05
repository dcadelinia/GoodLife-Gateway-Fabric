"""Smoke tests for health and root endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "HEALTHY"
    assert "version" in data


def test_healthz_alias():
    r = client.get("/healthz")
    assert r.status_code == 200


def test_root_online():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ONLINE"
    assert data["service"] == "GoodLife Gateway Fabric"
    assert data["nvidia_inception"] is True


def test_contact_accepts_valid():
    r = client.post(
        "/api/v1/contact",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "message": "Hello from test suite",
        },
    )
    assert r.status_code == 202
    assert r.json()["status"] == "received"


def test_telemetry_accepts():
    r = client.post(
        "/api/v1/telemetry",
        json={
            "route_uuid": "test-route-001",
            "node_id": "NODE-TEST",
            "efficiency_pct": 97.5,
        },
    )
    assert r.status_code == 202
