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
    audit.log("vbe.request", req.actor, {"action_id": req.action_id})
    return {"status": "PENDING_HUMAN_REVIEW", "action_id": req.action_id}

@router.post("/vbe/approve")
async def approve_vbe(req: VBERequest):
    if not req.approved:
        raise HTTPException(400, "approved must be true")
    audit.log("vbe.approved", req.actor, {"action_id": req.action_id})
    return {"status": "APPROVED", "action_id": req.action_id}
