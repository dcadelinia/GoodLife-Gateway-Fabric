"""Telemetry ingestion endpoints."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from app.core.audit import AuditLogger

logger = logging.getLogger("goodlife.telemetry")
router = APIRouter()
audit = AuditLogger()


class TelemetryPayload(BaseModel):
    route_uuid: str
    node_id: str = "UNKNOWN"
    hardware_fault_condition: bool = False
    efficiency_pct: float | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)


@router.post("/telemetry", status_code=status.HTTP_202_ACCEPTED)
async def ingest_telemetry(payload: TelemetryPayload):
    """Accept telemetry from edge nodes / simulation engines."""
    audit.log(
        event_type="telemetry.ingest",
        actor=payload.node_id,
        detail={
            "route_uuid": payload.route_uuid,
            "fault": payload.hardware_fault_condition,
            "efficiency_pct": payload.efficiency_pct,
        },
    )
    logger.info(
        "Telemetry received node=%s route=%s fault=%s",
        payload.node_id,
        payload.route_uuid,
        payload.hardware_fault_condition,
    )
    return {
        "status": "accepted",
        "route_uuid": payload.route_uuid,
        "node_id": payload.node_id,
    }
