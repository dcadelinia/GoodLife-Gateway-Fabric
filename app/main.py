import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.contact import router as contact_router
from app.api.health import router as health_router
from app.api.telemetry import router as telemetry_router
from app.api.vbe import router as vbe_router
from app.core.config import settings
from app.services.orchestrator import StateOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("goodlife")
orchestrator = StateOrchestrator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(orchestrator.run())
    logger.info("GoodLife Gateway Fabric started")
    try:
        yield
    finally:
        orchestrator.stop()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

app = FastAPI(
    title="GoodLife Gateway Fabric",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(telemetry_router, prefix="/api/v1")
app.include_router(contact_router, prefix="/api/v1")
app.include_router(vbe_router, prefix="/api/v1")

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
    }
