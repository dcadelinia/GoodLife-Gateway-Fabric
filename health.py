"""Health and readiness endpoints for Fly.io / load balancers."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, Response, status

from app.core.config import settings

router = APIRouter()


@router.get("/health")
@router.get("/healthz")
async def health(response: Response):
    """Primary health check – used by Dockerfile HEALTHCHECK and Fly.io."""
    heartbeat = Path(settings.HEARTBEAT_PATH)
    healthy = heartbeat.exists() and heartbeat.read_text(encoding="utf-8").strip() == "ACTIVE"
    if healthy:
        return {
            "status": "HEALTHY",
            "matrix_loop": "SYNCHRONIZED",
            "version": "1.2.0",
            "service": "GoodLife Gateway Fabric",
        }
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "status": "UNHEALTHY",
        "matrix_loop": "DE-SYNCHRONIZED",
        "version": "1.2.0",
    }


@router.get("/ready")
async def readiness():
    """Kubernetes-style readiness (same as health for Starter Kit)."""
    return await health(Response())
