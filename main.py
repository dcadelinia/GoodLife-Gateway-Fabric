"""
GoodLife Gateway Fabric – Primary FastAPI application.
Cloud control plane for Odynex Axis Logistics LLC Living Matrix.
NVIDIA Inception Program Member.
"""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import contact, health, telemetry, vbe
from app.core.audit import AuditLogger
from app.core.config import settings
from app.services.orchestrator import StateOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("goodlife.gateway")

audit = AuditLogger()
orchestrator = StateOrchestrator(audit=audit)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info(
        "GoodLife Gateway Fabric starting – env=%s version=%s",
        settings.ENVIRONMENT,
        settings.VERSION,
    )
    task = asyncio.create_task(orchestrator.run())
    audit.log(
        event_type="system.startup",
        actor="system",
        detail={"version": settings.VERSION, "env": settings.ENVIRONMENT},
    )
    try:
        yield
    finally:
        orchestrator.stop()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        audit.log(event_type="system.shutdown", actor="system", detail={})
        logger.info("GoodLife Gateway Fabric shut down cleanly")


app = FastAPI(
    title="GoodLife Gateway Fabric",
    description=(
        "Cloud control plane – Odynex Axis Logistics LLC · NVIDIA Inception. "
        "Founder: David Fabian Cadelinia · david@odynexaxis.biz · 229-364-1658"
    ),
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    audit.log(
        event_type="error.unhandled",
        actor="system",
        detail={"path": str(request.url.path), "error": str(exc)},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": "Internal server error"},
    )


# Mount routers
app.include_router(health.router, tags=["Health"])
app.include_router(telemetry.router, prefix="/api/v1", tags=["Telemetry"])
app.include_router(contact.router, prefix="/api/v1", tags=["Contact"])
app.include_router(vbe.router, prefix="/api/v1", tags=["Validation Before Execution"])


@app.get("/")
async def root():
    """Baseline handshake for load balancers and partners."""
    return {
        "status": "ONLINE",
        "service": "GoodLife Gateway Fabric",
        "version": settings.VERSION,
        "proprietor": "Odynex Axis Logistics LLC",
        "founder": "David Fabian Cadelinia",
        "nvidia_inception": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subsystems": {
            "orchestrator": "OPERATIONAL" if orchestrator.is_active else "STARTING",
            "audit": "ACTIVE",
            "vbe_gate": "READY",
        },
    }
