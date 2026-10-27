"""
GoodLife Gateway Fabric – Primary FastAPI application.
Cloud control plane for Odynex Axis Logistics LLC Living Matrix.
"""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import health, telemetry, contact, vbe
from app.core.config import settings
from app.core.audit import AuditLogger
from app.services.orchestrator import StateOrchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("goodlife.gateway")

# Shared runtime objects
audit = AuditLogger()
orchestrator = StateOrchestrator(audit=audit)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("GoodLife Gateway Fabric starting – environment=%s", settings.ENVIRONMENT)
    task = asyncio.create_task(orchestrator.run())
    audit.log(
        event_type="system.startup",
        actor="system",
        detail={"version": "1.2.0", "env": settings.ENVIRONMENT},
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
    description="Cloud control plane – Odynex Axis Logistics LLC · NVIDIA Inception",
    version="1.2.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url=None,
)

# CORS – tighten allow_origins in production via settings
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
        "version": "1.2.0",
        "proprietor": "Odynex Axis Logistics LLC",
        "nvidia_inception": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subsystems": {
            "orchestrator": "OPERATIONAL" if orchestrator.is_active else "STOPPED",
            "audit": "ACTIVE",
            "vbe_gate": "READY",
        },
    }
