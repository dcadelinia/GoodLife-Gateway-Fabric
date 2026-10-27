"""Telemetry ingestion tests."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_telemetry_ingest():
    payload = {
        "route_uuid": "route-test-001",
        "node_id": "FABRIC-ALBANY-MAIN",
        "hardware_fault_condition": False,
        "efficiency_pct": 92.5,
        "metrics": {"latency_ms": 12},
    }
    r = client.post("/api/v1/telemetry", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ACCEPTED"
    assert data["route_uuid"] == "route-test-001"
