import os
import json
import yaml
import asyncio
import signal
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Response, status

app = FastAPI(title="GoodLife Gateway Fabric - Omni Service Core")

# Thread-safe lifecycle variable
LOOP_ACTIVE = True

# Pydantic schemas for data validation
class TelemetryPayload(BaseModel):
    route_uuid: str
    hardware_fault_condition: bool

def read_loop_blueprint():
    try:
        if os.path.exists("safe_state_loops.yaml"):
            with open("safe_state_loops.yaml", "r") as stream:
                return yaml.safe_load(stream)
    except Exception as parse_error:
        print(f"BASELINE ERROR: Failing to parse blueprint: {parse_error}")
    return None

async def continuous_state_orchestrator():
    global LOOP_ACTIVE
    blueprint = read_loop_blueprint()
    
    print("Omni Service State loop tracking initialized successfully.")
    
    while LOOP_ACTIVE:
        try:
            # Simulate automation loop ticks
            await asyncio.sleep(0.5) 
            
            # Write dynamic loop heartbeat validation state out to temp space
            with open("/tmp/fabric_heartbeat.lock", "w") as lock_file:
                lock_file.write("ACTIVE")
            
            # Use interval configuration parameters if available, fallback to 5 seconds
            cooldown = blueprint["safety_limits"]["cooldown_interval_seconds"] if blueprint else 5
            await asyncio.sleep(cooldown)
            
        except asyncio.CancelledError:
            print("State orchestration loop safely intercepted and closed.")
            break
        except Exception as runtime_fault:
            print(f"Exception in state loop node: {runtime_fault}")
            await asyncio.sleep(5)

def intercept_sigterm(signum, frame):
    global LOOP_ACTIVE
    print("Fly.io SIGTERM detected. Executing graceful state conservation drain...")
    LOOP_ACTIVE = False

# Capture container infrastructure lifecycle termination triggers
signal.signal(signal.SIGTERM, intercept_sigterm)

@app.on_event("startup")
async def register_background_matrices():
    asyncio.create_task(continuous_state_orchestrator())

@app.get("/")
def baseline_handshake():
    return {
        "status": "ONLINE",
        "fabric_verification": "SUCCESS",
        "subsystems": {
            "omni_service": "OPERATIONAL"
        }
    }

@app.get("/healthz")
def platform_health_gate(response: Response):
    # Verifies both HTTP visibility and underlying async task loop state health
    if os.path.exists("/tmp/fabric_heartbeat.lock") and LOOP_ACTIVE:
        return {"status": "HEALTHY", "matrix_loop": "SYNCHRONIZED"}
    
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "UNHEALTHY", "matrix_loop": "DE-SYNCHRONIZED"}
