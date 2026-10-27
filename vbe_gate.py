"""
Validation Before Execution (VBE) Gate – JusticeTree-style human supervision.

No high-impact control action is executed until it passes this gate.
Starter Kit: records proposals and allows approve/reject.
Production: integrate with operator UI, multi-party approval, or policy engine.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from app.core.audit import AuditLogger

logger = logging.getLogger("goodlife.vbe")


class GateStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    EXPIRED = "EXPIRED"


class ActionProposal(BaseModel):
    proposal_id: str = Field(default_factory=lambda: str(uuid4()))
    action_type: str
    payload: Dict[str, Any]
    requested_by: str
    reason: str = ""
    status: GateStatus = GateStatus.PENDING
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    decided_by: Optional[str] = None
    decided_at: Optional[str] = None
    decision_note: Optional[str] = None


class VBEGate:
    """In-memory gate for Starter Kit. Replace with durable store for production."""

    def __init__(self, audit: AuditLogger) -> None:
        self.audit = audit
        self._proposals: Dict[str, ActionProposal] = {}

    def propose(
        self,
        action_type: str,
        payload: Dict[str, Any],
        requested_by: str,
        reason: str = "",
    ) -> ActionProposal:
        proposal = ActionProposal(
            action_type=action_type,
            payload=payload,
            requested_by=requested_by,
            reason=reason,
        )
        self._proposals[proposal.proposal_id] = proposal
        self.audit.log(
            event_type="vbe.propose",
            actor=requested_by,
            resource=proposal.proposal_id,
            detail={"action_type": action_type, "reason": reason},
            decision="PENDING",
        )
        logger.info("VBE proposal created: %s (%s)", proposal.proposal_id, action_type)
        return proposal

    def decide(
        self,
        proposal_id: str,
        approved: bool,
        decided_by: str,
        note: str = "",
    ) -> ActionProposal:
        if proposal_id not in self._proposals:
            raise KeyError(f"Unknown proposal: {proposal_id}")
        proposal = self._proposals[proposal_id]
        if proposal.status != GateStatus.PENDING:
            raise ValueError(f"Proposal already decided: {proposal.status}")

        proposal.status = GateStatus.APPROVED if approved else GateStatus.REJECTED
        proposal.decided_by = decided_by
        proposal.decided_at = datetime.now(timezone.utc).isoformat()
        proposal.decision_note = note

        self.audit.log(
            event_type="vbe.decide",
            actor=decided_by,
            resource=proposal_id,
            detail={"approved": approved, "note": note},
            decision=proposal.status.value,
        )
        logger.info(
            "VBE decision: %s -> %s by %s",
            proposal_id,
            proposal.status.value,
            decided_by,
        )
        return proposal

    def mark_executed(self, proposal_id: str, executor: str) -> ActionProposal:
        proposal = self._proposals[proposal_id]
        if proposal.status != GateStatus.APPROVED:
            raise ValueError("Only APPROVED proposals may be executed")
        proposal.status = GateStatus.EXECUTED
        self.audit.log(
            event_type="vbe.execute",
            actor=executor,
            resource=proposal_id,
            detail={"action_type": proposal.action_type},
            decision="EXECUTED",
        )
        return proposal

    def get(self, proposal_id: str) -> Optional[ActionProposal]:
        return self._proposals.get(proposal_id)

    def list_pending(self) -> list[ActionProposal]:
        return [p for p in self._proposals.values() if p.status == GateStatus.PENDING]
