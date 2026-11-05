"""Health endpoints – always 200 when the process is alive (required for Fly smoke checks)."""
from __future__ import annotations
from pathlib import Path
from fastapi import APIRouter, Response
from app.core.config import settings

router = APIRouter()

@router.get("/health")
@router.get("/healthz")
async def health(response: Response):
    heartbeat = Path(settings.HEARTBEAT_PATH)
    has_hb = heartbeat.exists() and heartbeat.read_text(encoding="utf-8").strip() == "ACTIVE"
    return {
        "status": "HEALTHY",
        "matrix_loop": "SYNCHRONIZED" if has_hb else "STARTING",
        "version": settings.VERSION,
        "service": settings.APP_NAME,
        "company": "Odynex Axis Logistics LLC",
    }

@router.get("/ready")
async def readiness():
    return await health(Response())
