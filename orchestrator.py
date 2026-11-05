import asyncio
from pathlib import Path
from app.core.config import settings
class StateOrchestrator:
    def __init__(self, audit=None):
        self._active = False
        self._stop = asyncio.Event()
    @property
    def is_active(self):
        return self._active
    def stop(self):
        self._stop.set()
    async def run(self):
        self._active = True
        path = Path(settings.HEARTBEAT_PATH)
        try:
            while not self._stop.is_set():
                try:
                    path.write_text("ACTIVE")
                except Exception:
                    pass
                try:
                    await asyncio.wait_for(self._stop.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    pass
        finally:
            self._active = False
