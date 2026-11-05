import asyncio, logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import contact, health, telemetry, vbe
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

app = FastAPI(title="GoodLife Gateway Fabric", version=settings.VERSION, lifespan=lifespan, docs_url=None)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(telemetry.router, prefix="/api/v1")
app.include_router(contact.router, prefix="/api/v1")
app.include_router(vbe.router, prefix="/api/v1")

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
