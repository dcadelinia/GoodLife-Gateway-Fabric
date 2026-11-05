from pathlib import Path

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()

@router.get("/health")
@router.get("/healthz")
async def health():
    heartbeat_path = Path(settings.HEARTBEAT_PATH)
    heartbeat = heartbeat_path.exists() and heartbeat_path.read_text(encoding="utf-8").strip() == "ACTIVE"
    return {
        "status": "HEALTHY",
        "matrix_loop": "SYNCHRONIZED" if heartbeat else "STARTING",
        "version": settings.VERSION,
        "service": settings.APP_NAME,
    }

@router.get("/ready")
async def ready():
    return {"status": "READY", "service": settings.APP_NAME, "version": settings.VERSION}
