"""
Continuous state orchestrator – Möbius-loop style heartbeat and node awareness.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Optional

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
        self._active = True
        self._stop.clear()
        logger.info("State orchestrator started (interval=%.1fs)", settings.ORCHESTRATOR_INTERVAL_SEC)
        try:
            while not self._stop.is_set():
                self._write_heartbeat()
                await asyncio.sleep(settings.ORCHESTRATOR_INTERVAL_SEC)
        except asyncio.CancelledError:
            logger.info("Orchestrator cancelled")
        finally:
            self._active = False
            self._remove_heartbeat()
            logger.info("State orchestrator stopped")

    def _write_heartbeat(self) -> None:
        path = Path(settings.HEARTBEAT_PATH)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("ACTIVE", encoding="utf-8")
        except OSError as e:
            logger.warning("Could not write heartbeat: %s", e)

    def _remove_heartbeat(self) -> None:
        try:
            Path(settings.HEARTBEAT_PATH).unlink(missing_ok=True)
        except OSError:
            pass

    def load_manifest(self) -> dict:
        """Load gateway routing manifest if present."""
        candidates = [
            Path("system_config/gateway_manifest.json"),
            Path("config/gateway_manifest.json"),
        ]
        for p in candidates:
            if p.exists():
                try:
                    return json.loads(p.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError) as e:
                    logger.warning("Manifest read error: %s", e)
        return {
            "system_layer": "GoodLife-Gateway-Fabric",
            "compute_engine": "NVIDIA-Inception-Accelerated-Mesh",
            "routing_nodes": [],
        }
