"""Validation Before Execution (VBE) gate – human-supervised control actions."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.audit import AuditLogger

router = APIRouter()
audit = AuditLogger()


class VBERequest(BaseModel):
    action_id: str = Field(..., min_length=1)
    description: str
    actor: str = "operator"
    approved: bool = False


@router.post("/vbe/request")
async def request_vbe(req: VBERequest):
    """Submit an action for Validation Before Execution."""
    audit.log(
        event_type="vbe.request",
        actor=req.actor,
        detail={"action_id": req.action_id, "description": req.description},
    )
    return {
        "status": "PENDING_HUMAN_REVIEW",
        "action_id": req.action_id,
        "message": "Action held at VBE gate until human approval.",
    }


@router.post("/vbe/approve")
async def approve_vbe(req: VBERequest):
    if not req.approved:
        raise HTTPException(status_code=400, detail="approved must be true")
    audit.log(
        event_type="vbe.approved",
        actor=req.actor,
        detail={"action_id": req.action_id},
    )
    return {
        "status": "APPROVED",
        "action_id": req.action_id,
        "message": "Action cleared Validation Before Execution gate.",
    }
