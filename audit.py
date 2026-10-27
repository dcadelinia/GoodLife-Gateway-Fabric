"""
Immutable audit trail (Starter Kit implementation).

In production replace the file backend with an append-only store,
ledger, or managed audit service. Events are never mutated or deleted.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

logger = logging.getLogger("goodlife.audit")


class AuditLogger:
    def __init__(self, log_dir: str = "logs/audit") -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._file = self.log_dir / "audit_events.jsonl"

    def log(
        self,
        event_type: str,
        actor: str,
        detail: Optional[Dict[str, Any]] = None,
        decision: Optional[str] = None,
        resource: Optional[str] = None,
    ) -> str:
        """Append an immutable audit event. Returns event_id."""
        event_id = str(uuid4())
        record = {
            "event_id": event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "actor": actor,
            "resource": resource,
            "decision": decision,
            "detail": detail or {},
        }
        line = json.dumps(record, ensure_ascii=False) + "\n"
        with self._lock:
            with open(self._file, "a", encoding="utf-8") as f:
                f.write(line)
        logger.info("AUDIT %s | %s | %s", event_type, actor, event_id)
        return event_id

    def recent(self, limit: int = 50) -> list[dict]:
        """Read the last N events (for operator dashboards)."""
        if not self._file.exists():
            return []
        with self._lock:
            lines = self._file.read_text(encoding="utf-8").strip().splitlines()
        events = []
        for line in lines[-limit:]:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return events
