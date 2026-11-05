from __future__ import annotations
import asyncio, logging
from pathlib import Path
from app.core.audit import AuditLogger
from app.core.config import settings
logger = logging.getLogger("goodlife.orchestrator")

class StateOrchestrator:
    def __init__(self, audit: AuditLogger) -> None:
        self.audit = audit
        self._active = False
        self._stop = asyncio.Event()
    @property
    def is_active(self) -> bool:
        return self._active
    def stop(self) -> None:
        self._stop.set()
    async def run(self) -> None:
        path = Path(settings.HEARTBEAT_PATH)
        self._active = True
        try:
            while not self._stop.is_set():
                try:
                    path.write_text("ACTIVE", encoding="utf-8")
                except Exception:
                    pass
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    pass
        finally:
            self._active = False
