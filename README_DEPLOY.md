# GoodLife Gateway Fabric – Deploy-Ready Fix Package

**Odynex Axis Logistics LLC** · NVIDIA Inception  
Founder: David Fabian Cadelinia · david@odynexaxis.biz · 229-364-1658

This package fixes the Fly.io build failure caused by a corrupted `requirements.txt`
(it contained markdown / bash instructions instead of Python packages) and ensures
a complete, runnable FastAPI application layout that matches the Dockerfile CMD.

---

## What was broken

```
ERROR: Invalid requirement: '```bash': Expected package name at the start of
dependency specifier
    ```bash
    ^ (from line 7 of requirements.txt)
```

The repository’s `requirements.txt` had been overwritten with deploy instructions.
In addition, the expected `app/` package (referenced by `uvicorn app.main:app`)
was missing or incomplete, causing runtime crashes after a successful build.

---

## What this package contains

```
goodlife-gateway-fabric-fixed/
├── app/
│   ├── __init__.py
│   ├── main.py              ← FastAPI app (uvicorn app.main:app)
│   ├── api/
│   │   ├── health.py        ← /health always 200 when process is up
│   │   ├── contact.py
│   │   ├── telemetry.py
│   │   └── vbe.py           ← Validation-Before-Execution gate
│   ├── core/
│   │   ├── config.py
│   │   └── audit.py
│   └── services/
│       └── orchestrator.py  ← writes heartbeat for health checks
├── tests/
│   └── test_health.py
├── Dockerfile               ← multi-stage, binds 0.0.0.0:8080
├── fly.toml                 ← explicit health check + grace period
├── requirements.txt         ← valid pip dependencies only
├── .dockerignore
└── README_DEPLOY.md         ← this file
```

---

## Deploy steps (copy-paste)

```bash
# 1. Unzip into a clean directory (or replace your existing deploy tree)
unzip goodlife-gateway-fabric-fixed.zip -d goodlife-gateway-fabric-fixed
cd goodlife-gateway-fabric-fixed

# 2. Confirm critical files
ls Dockerfile fly.toml requirements.txt app/main.py

# 3. (Recommended) set / rotate secrets
fly secrets set \
  SECRET_KEY="$(openssl rand -hex 32)" \
  JWT_SECRET="$(openssl rand -hex 32)" \
  -a goodlife-gateway-fabric-vmbi4w

# 4. Deploy (builds a new image from the Dockerfile in this directory)
fly deploy -a goodlife-gateway-fabric-vmbi4w

# 5. Watch the rolling update
fly status -a goodlife-gateway-fabric-vmbi4w
fly logs -a goodlife-gateway-fabric-vmbi4w

# 6. Verify smoke-check endpoints
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/health
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/
```

Expected health response:

```json
{
  "status": "HEALTHY",
  "matrix_loop": "SYNCHRONIZED",
  "version": "1.2.0",
  "service": "GoodLife Gateway Fabric",
  "company": "Odynex Axis Logistics LLC"
}
```

---

## Local verification before deploy

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080

# in another terminal:
curl http://localhost:8080/health
curl http://localhost:8080/
pytest tests/ -v
```

---

## If machines are stuck

```bash
fly machines list -a goodlife-gateway-fabric-vmbi4w
fly machines destroy <id> --force   # only if needed
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

---

## Endpoints available after deploy

| Method | Path                     | Purpose                          |
|--------|--------------------------|----------------------------------|
| GET    | `/`                      | Root handshake                   |
| GET    | `/health` `/healthz`     | Liveness (always 200 when up)    |
| GET    | `/ready`                 | Readiness                        |
| POST   | `/api/v1/telemetry`      | Edge / simulation telemetry      |
| POST   | `/api/v1/contact`        | Contact / lead form              |
| POST   | `/api/v1/vbe/propose`    | Submit action for human approval |
| POST   | `/api/v1/vbe/{id}/decide`| Approve / reject proposal        |
| GET    | `/api/v1/vbe`            | List proposals                   |

---

© 2026 Odynex Axis Logistics LLC. All rights reserved.
