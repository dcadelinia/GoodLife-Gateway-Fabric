from fastapi import FastAPI
import os
import yaml

app = FastAPI(title="Odynexaxis Trade App")

# Load safe_state_loops configuration if needed by your logic
@app.on_event("startup")
async def startup_event():
    blueprint_path = "safe_state_loops.yaml"
    if os.path.exists(blueprint_path):
        with open(blueprint_path, "r") as f:
            print("Loaded safe_state_loops.yaml configuration layout successfully.")
    else:
        print("Warning: safe_state_loops.yaml layout blueprint not found.")

@app.get("/")
def read_root():
    return {"status": "healthy", "app": "odynexaxis-trade-app"}

@app.get("/healthz")
def health_check():
    return {"status": "OK"}
  
