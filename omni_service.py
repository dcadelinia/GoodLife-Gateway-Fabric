# Use a slim, stable base Python image
FROM python:3.11-slim

# Force root directory bounds inside the container
WORKDIR /app

# Ensure Python looks inside /app so your custom modules import flawlessly
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install dependencies cleanly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all core files, YAML blueprints, and project directories into the image
COPY . .

# EXPOSE port 8080 to match your fly.toml configuration
EXPOSE 8080

# CRITICAL FIX: Run directly through omni_service.py where your app context is defined
CMD ["uvicorn", "omni_service:app", "--host", "0.0.0.0", "--port", "8080"]
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
