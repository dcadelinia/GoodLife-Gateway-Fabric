"""Lightweight immutable audit logger."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("goodlife.audit")


class AuditLogger:
    def log(
        self,
        event_type: str,
        actor: str = "system",
        detail: dict[str, Any] | None = None,
    ) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event": event_type,
            "actor": actor,
            "detail": detail or {},
        }
        logger.info("AUDIT %s", json.dumps(record, default=str))
