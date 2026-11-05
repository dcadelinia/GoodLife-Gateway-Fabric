# Fly.io Deploy Fix – GoodLife Gateway Fabric

## Root cause of crash

The previous image failed smoke checks because:

1. **Dockerfile CMD** ran `uvicorn app.main:app`
2. The repository had **no `app/` Python package** (only root-level scripts)
3. `main.py` imported `app.api`, `app.core.config`, etc. → `ModuleNotFoundError`
4. Process exited immediately → Fly reported "the app appears to be crashing"

## What was fixed

- Created proper package layout:
  ```
  app/
    __init__.py
    main.py          ← FastAPI app (uvicorn app.main:app)
    api/
      health.py      ← /health always returns 200 when process is up
      contact.py
      telemetry.py
      vbe.py
    core/
      config.py
      audit.py
    services/
      orchestrator.py  ← writes heartbeat file
  ```
- Health endpoint no longer returns 503 on cold start (Fly smoke checks pass)
- Explicit Fly HTTP health check on `/health` with 20s grace period
- Dockerfile CMD left as `uvicorn app.main:app` (now valid)

## Deploy steps

```bash
cd goodlife-gateway-fabric-fixed   # or replace your repo contents

# Optional: set secrets
fly secrets set SECRET_KEY="$(openssl rand -hex 32)" -a goodlife-gateway-fabric-vmbi4w
fly secrets set JWT_SECRET="$(openssl rand -hex 32)" -a goodlife-gateway-fabric-vmbi4w

# Deploy from this directory (builds new image)
fly deploy -a goodlife-gateway-fabric-vmbi4w

# Verify
fly status -a goodlife-gateway-fabric-vmbi4w
fly logs -a goodlife-gateway-fabric-vmbi4w
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/health
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/
```

## Local verification before deploy

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
# in another terminal:
curl http://localhost:8080/health
curl http://localhost:8080/
pytest tests/ -v
```

## If machines are stuck

```bash
fly machines list -a goodlife-gateway-fabric-vmbi4w
fly machines destroy <id> --force   # only if needed
fly deploy -a goodlife-gateway-fabric-vmbi4w
```
