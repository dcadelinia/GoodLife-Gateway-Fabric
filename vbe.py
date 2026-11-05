"""Validation Before Execution (VBE) gate – human-in-the-loop control."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.audit import AuditLogger

logger = logging.getLogger("goodlife.vbe")
router = APIRouter()
audit = AuditLogger()

# In-memory store for demo / single-instance deploy.
# Replace with Redis / Postgres for multi-machine production.
_proposals: dict[str, dict[str, Any]] = {}


class VBEProposalRequest(BaseModel):
    action_type: str
    payload: dict[str, Any]
    reason: str = ""
    requested_by: str = "operator"


class VBEDecisionRequest(BaseModel):
    approved: bool
    decided_by: str
    note: str = ""


@router.post("/vbe/propose", status_code=status.HTTP_201_CREATED)
async def propose_action(req: VBEProposalRequest):
    """Submit an action for Validation-Before-Execution review."""
    proposal_id = str(uuid.uuid4())
    record = {
        "id": proposal_id,
        "action_type": req.action_type,
        "payload": req.payload,
        "reason": req.reason,
        "requested_by": req.requested_by,
        "status": "PENDING",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "decision": None,
    }
    _proposals[proposal_id] = record
    audit.log(
        event_type="vbe.proposed",
        actor=req.requested_by,
        detail={"proposal_id": proposal_id, "action_type": req.action_type},
    )
    logger.info("VBE proposal %s type=%s by %s", proposal_id, req.action_type, req.requested_by)
    return {"status": "pending", "proposal_id": proposal_id}


@router.post("/vbe/{proposal_id}/decide")
async def decide_action(proposal_id: str, req: VBEDecisionRequest):
    """Approve or reject a pending proposal."""
    if proposal_id not in _proposals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    record = _proposals[proposal_id]
    if record["status"] != "PENDING":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already decided")
    record["status"] = "APPROVED" if req.approved else "REJECTED"
    record["decision"] = {
        "approved": req.approved,
        "decided_by": req.decided_by,
        "note": req.note,
        "decided_at": datetime.now(timezone.utc).isoformat(),
    }
    audit.log(
        event_type="vbe.decided",
        actor=req.decided_by,
        detail={
            "proposal_id": proposal_id,
            "approved": req.approved,
            "note": req.note,
        },
    )
    return {"status": record["status"], "proposal_id": proposal_id}


@router.get("/vbe/{proposal_id}")
async def get_proposal(proposal_id: str):
    if proposal_id not in _proposals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    return _proposals[proposal_id]


@router.get("/vbe")
async def list_proposals():
    return {"proposals": list(_proposals.values())}
