"""Validation Before Execution API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.audit import AuditLogger
from app.core.vbe_gate import VBEGate
from app.models.schemas import VBEDecisionRequest, VBEProposalRequest

router = APIRouter()
_audit = AuditLogger()
_gate = VBEGate(audit=_audit)


@router.post("/vbe/propose")
async def propose_action(body: VBEProposalRequest):
    proposal = _gate.propose(
        action_type=body.action_type,
        payload=body.payload,
        requested_by=body.requested_by,
        reason=body.reason,
    )
    return {"status": "PENDING", "proposal": proposal.model_dump()}


@router.post("/vbe/{proposal_id}/decide")
async def decide_action(proposal_id: str, body: VBEDecisionRequest):
    try:
        proposal = _gate.decide(
            proposal_id=proposal_id,
            approved=body.approved,
            decided_by=body.decided_by,
            note=body.note,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Proposal not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": proposal.status.value, "proposal": proposal.model_dump()}


@router.get("/vbe/pending")
async def list_pending():
    pending = _gate.list_pending()
    return {"count": len(pending), "proposals": [p.model_dump() for p in pending]}


@router.get("/vbe/{proposal_id}")
async def get_proposal(proposal_id: str):
    proposal = _gate.get(proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal.model_dump()
