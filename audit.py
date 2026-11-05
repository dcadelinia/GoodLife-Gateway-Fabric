import json, logging
from datetime import datetime, timezone
logger = logging.getLogger("goodlife.audit")
class AuditLogger:
    def log(self, event_type, actor="system", detail=None):
        logger.info("AUDIT %s", json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "event": event_type, "actor": actor, "detail": detail or {}}))
