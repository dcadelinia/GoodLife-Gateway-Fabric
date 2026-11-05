"""Telemetry ingestion."""
from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.core.audit import AuditLogger

router = APIRouter()
audit = AuditLogger()

class TelemetryPayload(BaseModel):
    route_uuid: str = Field(..., min_length=1)
    hardware_fault_condition: bool = False
    metrics: dict | None = None

@router.post("/telemetry")
async def ingest_telemetry(payload: TelemetryPayload):
    audit.log(event_type="telemetry.ingest", actor="edge", detail={"route_uuid": payload.route_uuid, "fault": payload.hardware_fault_condition})
    return {"status": "ACCEPTED", "route_uuid": payload.route_uuid}
