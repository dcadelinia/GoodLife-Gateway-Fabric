# GoodLife Gateway Fabric – Complete Deploy Fix Package

**Odynex Axis Logistics LLC** · NVIDIA Inception  
Founder: David Fabian Cadelinia · david@odynexaxis.biz · 229-364-1658

This package fixes the Fly.io build failure caused by a corrupted `requirements.txt`
(it contained markdown / bash instructions instead of Python packages) and provides
a complete, runnable FastAPI control-plane that deploys cleanly on Fly.io.

Also included:
- Full stack recommendations (Python control plane + optional Next.js frontend)
- GitHub Actions workflow
- Pre/post deploy checklists
- Local verification tests

---

## Quick start

```bash
unzip goodlife-complete-fix.zip -d goodlife-complete-fix
cd goodlife-complete-fix

fly secrets set \
  SECRET_KEY="$(openssl rand -hex 32)" \
  JWT_SECRET="$(openssl rand -hex 32)" \
  -a goodlife-gateway-fabric-vmbi4w

fly deploy -a goodlife-gateway-fabric-vmbi4w

curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/health
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/
```

Full details: **DEPLOY.md** and **CHECKLIST.md**

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

## Package layout

```
goodlife-complete-fix/
├── app/
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
├── .github/workflows/
│   └── fly-deploy.yml       ← auto-deploy on push to main
├── Dockerfile               ← multi-stage, pure Python, binds 0.0.0.0:8080
├── fly.toml                 ← explicit health check + 25 s grace
├── requirements.txt         ← valid pip dependencies only
├── env.example
├── DEPLOY.md                ← step-by-step deploy guide
├── CHECKLIST.md             ← pre / post deploy checklist
├── STACK_RECOMMENDATIONS.md ← Python + optional Next.js architecture
└── README_DEPLOY.md         ← this file
```

---

## Endpoints after successful deploy

| Method | Path                      | Purpose                          |
|--------|---------------------------|----------------------------------|
| GET    | `/`                       | Root handshake                   |
| GET    | `/health` `/healthz`      | Liveness (always 200 when up)    |
| GET    | `/ready`                  | Readiness                        |
| POST   | `/api/v1/telemetry`       | Edge / simulation telemetry      |
| POST   | `/api/v1/contact`         | Contact / lead form              |
| POST   | `/api/v1/vbe/propose`     | Submit action for human approval |
| POST   | `/api/v1/vbe/{id}/decide` | Approve / reject proposal        |
| GET    | `/api/v1/vbe`             | List proposals                   |

---

## Local verification

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
# another terminal
curl http://localhost:8080/health
pytest tests/ -v
```

---

## Stack guidance

See **STACK_RECOMMENDATIONS.md** for:
- Why this Python control plane is the primary deploy target
- How to add a Next.js + Prisma + Stripe frontend later
- Database, secrets, and scaling recommendations
- What **not** to mix into the same Docker image

---

© 2026 Odynex Axis Logistics LLC. All rights reserved.
