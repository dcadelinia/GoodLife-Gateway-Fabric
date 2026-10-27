"""Validation Before Execution gate tests."""

from app.core.audit import AuditLogger
from app.core.vbe_gate import VBEGate, GateStatus


def test_propose_and_approve():
    audit = AuditLogger(log_dir="logs/audit_test")
    gate = VBEGate(audit=audit)

    proposal = gate.propose(
        action_type="route_change",
        payload={"from": "A", "to": "B"},
        requested_by="operator1",
        reason="Load balancing",
    )
    assert proposal.status == GateStatus.PENDING

    decided = gate.decide(
        proposal_id=proposal.proposal_id,
        approved=True,
        decided_by="supervisor1",
        note="Approved after review",
    )
    assert decided.status == GateStatus.APPROVED
    assert decided.decided_by == "supervisor1"

    executed = gate.mark_executed(proposal.proposal_id, executor="system")
    assert executed.status == GateStatus.EXECUTED


def test_reject():
    audit = AuditLogger(log_dir="logs/audit_test")
    gate = VBEGate(audit=audit)
    p = gate.propose("node_isolation", {"node_id": "X"}, "op")
    d = gate.decide(p.proposal_id, approved=False, decided_by="sup", note="Unsafe")
    assert d.status == GateStatus.REJECTED
