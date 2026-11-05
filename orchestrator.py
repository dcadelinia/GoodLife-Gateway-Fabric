"""Continuous state orchestrator – writes heartbeat for health checks."""

from __future__ import annotations

import asyncio
import logging
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
        """Write heartbeat every few seconds so /health stays green."""
        path = Path(settings.HEARTBEAT_PATH)
        self._active = True
        logger.info("StateOrchestrator started – heartbeat=%s", path)
        try:
            while not self._stop.is_set():
                try:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("ACTIVE", encoding="utf-8")
                except Exception as exc:
                    logger.warning("Failed to write heartbeat: %s", exc)
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    pass
        finally:
            self._active = False
            try:
                if path.exists():
                    path.unlink()
            except Exception:
                pass
            logger.info("StateOrchestrator stopped")
