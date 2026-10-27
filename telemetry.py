"""Telemetry ingestion endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.audit import AuditLogger
from app.models.schemas import TelemetryPayload

router = APIRouter()
# Will be injected via app state in production; for simplicity use module-level
_audit = AuditLogger()


@router.post("/telemetry")
async def ingest_telemetry(payload: TelemetryPayload, request: Request):
    """Accept edge / field telemetry from Cycle Nodes."""
    _audit.log(
        event_type="telemetry.ingest",
        actor=payload.node_id,
        resource=payload.route_uuid,
        detail={
            "hardware_fault": payload.hardware_fault_condition,
            "efficiency_pct": payload.efficiency_pct,
            "metrics_keys": list(payload.metrics.keys()),
        },
    )
    return {
        "status": "ACCEPTED",
        "route_uuid": payload.route_uuid,
        "message": "Telemetry recorded into fabric audit trail",
    }
