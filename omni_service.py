import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize system
app = FastAPI(
    title="GoodLife Gateway Fabric",
    description="Unified API Layer for Odynex Axis Logistics LLC Frameworks",
    version="1.0.0"
)

# Standardized CORS Configuration (No longer using the root dot-notation directory)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core paths mapped directly to your new consolidated directories
COGNITIVE_LAYER_DIR = os.path.join(os.path.dirname(__file__), "cognitive_layer", "models")
QUANT_SPEC_PATH = os.path.join(COGNITIVE_LAYER_DIR, "quantization_spec.json")
GR00T_CONFIG_PATH = os.path.join(COGNITIVE_LAYER_DIR, "isaac_gr00t_config.json")

class TelemetryPayload(BaseModel):
    route_uuid: str
    accumulated_context_tokens: int
    freight_density_index: float
    hardware_fault_condition: bool

@app.get("/health")
def health_check():
    """Verifies service readiness and file system path integrity."""
    quant_exists = os.path.exists(QUANT_SPEC_PATH)
    gr00t_exists = os.path.exists(GR00T_CONFIG_PATH)
    
    if not (quant_exists and gr00t_exists):
        raise HTTPException(
            status_code=500, 
            detail="System misconfiguration: Hardware specs or GR00T policies missing from cognitive_layer/models/"
        )
    
    return {
        "status": "ONLINE",
        "fabric_verification": "SUCCESS",
        "subsystems": {
            "quantization_spec": "LOADED",
            "isaac_gr00t_policy": "LOADED"
        }
    }

@app.post("/api/v1/telemetry/orchestrated-route")
def process_edge_telemetry(payload: TelemetryPayload):
    """Processes incoming data frames against localized hardware manifests."""
    try:
        with open(QUANT_SPEC_PATH, 'r') as q_file:
            quant_data = json.load(q_file)
        with open(GR00T_CONFIG_PATH, 'r') as g_file:
            gr00t_data = json.load(g_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read local manifest maps: {str(e)}")

    # Deterministic network offload & routing response layout
    response = {
        "status": "PROCESSED",
        "pipeline_uuid": payload.route_uuid,
        "infrastructure": {
            "prefill_target": quant_data["model_deployment_manifest"]["hardware_mapping"]["prefill_cluster"],
            "decode_target": quant_data["model_deployment_manifest"]["hardware_mapping"]["decode_accelerator"]
        },
        "robotics_layer": {
            "policy": gr00t_data["isaac_gr00t_deployment"]["policy_target"],
            "safety_state": "ACTIVE"
        }
    }

    if payload.hardware_fault_condition:
        response["fault_mitigation"] = {
            "action": "ENGAGE_SHADOW_ENGINE",
            "actuator_override": gr00t_data["isaac_gr00t_deployment"]["actuation_safe_states"]["on_anomalous_fault"]
        }

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("omni_service.py:app", host="0.0.0.0", port=8000, reload=True)
