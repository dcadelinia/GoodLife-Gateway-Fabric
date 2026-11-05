from __future__ import annotations
import asyncio, logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import contact, health, telemetry, vbe
from app.core.audit import AuditLogger
from app.core.config import settings
from app.services.orchestrator import StateOrchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("goodlife.gateway")
audit = AuditLogger()
orchestrator = StateOrchestrator(audit=audit)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s v%s", settings.APP_NAME, settings.VERSION)
    task = asyncio.create_task(orchestrator.run())
    try:
        yield
    finally:
        orchestrator.stop()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

app = FastAPI(title="GoodLife Gateway Fabric", version=settings.VERSION, lifespan=lifespan, docs_url=None)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])

@app.exception_handler(Exception)
async def _err(request: Request, exc: Exception):
    logger.exception("error on %s", request.url.path)
    return JSONResponse(status_code=500, content={"status": "error", "message": "Internal server error"})

app.include_router(health.router, tags=["Health"])
app.include_router(telemetry.router, prefix="/api/v1", tags=["Telemetry"])
app.include_router(contact.router, prefix="/api/v1", tags=["Contact"])
app.include_router(vbe.router, prefix="/api/v1", tags=["VBE"])

@app.get("/")
async def root():
    return {
        "status": "ONLINE",
        "service": "GoodLife Gateway Fabric",
        "version": settings.VERSION,
        "proprietor": "Odynex Axis Logistics LLC",
        "founder": "David Fabian Cadelinia",
        "nvidia_inception": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subsystems": {"orchestrator": "OPERATIONAL" if orchestrator.is_active else "STARTING", "audit": "ACTIVE", "vbe_gate": "READY"},
    }
