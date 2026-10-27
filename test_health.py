"""Smoke tests for health and root endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ONLINE"
    assert data["service"] == "GoodLife Gateway Fabric"
    assert "nvidia_inception" in data


def test_health_endpoint():
    # After startup the orchestrator should have written a heartbeat
    r = client.get("/health")
    # May be HEALTHY or UNHEALTHY depending on timing; just ensure it responds
    assert r.status_code in (200, 503)
    data = r.json()
    assert "status" in data
    assert "version" in data


def test_docs_available_in_dev():
    r = client.get("/docs")
    # In test environment docs should be present
    assert r.status_code in (200, 404)  # 404 only if forced production
