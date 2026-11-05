from pathlib import Path
from fastapi import APIRouter
from app.core.config import settings
router = APIRouter()
@router.get("/health")
@router.get("/healthz")
async def health():
    hb = Path(settings.HEARTBEAT_PATH)
    ok = hb.exists() and hb.read_text().strip() == "ACTIVE"
    return {"status": "HEALTHY", "matrix_loop": "SYNCHRONIZED" if ok else "STARTING", "version": settings.VERSION, "service": settings.APP_NAME}
