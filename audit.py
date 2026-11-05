from __future__ import annotations
import json, logging
from datetime import datetime, timezone
from typing import Any
logger = logging.getLogger("goodlife.audit")

class AuditLogger:
    def log(self, event_type: str, actor: str = "system", detail: dict[str, Any] | None = None) -> None:
        logger.info("AUDIT %s", json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "event": event_type, "actor": actor, "detail": detail or {}}, default=str))
