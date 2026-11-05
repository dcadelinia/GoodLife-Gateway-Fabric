from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class TelemetryPayload(BaseModel):
    route_uuid: str = Field(..., min_length=1)
    node_id: str = Field(default="NODE-UNKNOWN", min_length=1)
    efficiency_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    hardware_fault_condition: bool = False

@router.post("/telemetry")
async def ingest(payload: TelemetryPayload):
    return {
        "status": "ACCEPTED",
        "route_uuid": payload.route_uuid,
        "node_id": payload.node_id,
        "efficiency_pct": payload.efficiency_pct,
    }
