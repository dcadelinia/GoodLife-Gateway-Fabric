from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.core.audit import AuditLogger
router = APIRouter()
audit = AuditLogger()

class TelemetryPayload(BaseModel):
    route_uuid: str = Field(..., min_length=1)
    hardware_fault_condition: bool = False

@router.post("/telemetry")
async def ingest(payload: TelemetryPayload):
    audit.log("telemetry.ingest", "edge", {"route_uuid": payload.route_uuid})
    return {"status": "ACCEPTED", "route_uuid": payload.route_uuid}
