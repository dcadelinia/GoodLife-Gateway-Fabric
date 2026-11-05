from fastapi import APIRouter
from pydantic import BaseModel, Field
router = APIRouter()
class TelemetryPayload(BaseModel):
    route_uuid: str = Field(..., min_length=1)
    hardware_fault_condition: bool = False
@router.post("/telemetry")
async def ingest(payload: TelemetryPayload):
    return {"status": "ACCEPTED", "route_uuid": payload.route_uuid}
