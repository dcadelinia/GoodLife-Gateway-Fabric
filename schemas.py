"""Request / response schemas."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field


class TelemetryPayload(BaseModel):
    route_uuid: str
    node_id: str = "UNKNOWN"
    hardware_fault_condition: bool = False
    efficiency_pct: Optional[float] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=5000)
    organization: Optional[str] = None


class VBEProposalRequest(BaseModel):
    action_type: str
    payload: Dict[str, Any]
    reason: str = ""
    requested_by: str = "operator"


class VBEDecisionRequest(BaseModel):
    approved: bool
    decided_by: str
    note: str = ""


class HealthResponse(BaseModel):
    status: str
    matrix_loop: str
    version: str = "1.2.0"
