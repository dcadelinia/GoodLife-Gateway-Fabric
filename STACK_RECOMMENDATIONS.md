# Stack Recommendations – GoodLife Gateway Fabric

**Odynex Axis Logistics LLC** · NVIDIA Inception  
Founder: David Fabian Cadelinia · david@odynexaxis.biz

This document describes the recommended production architecture and how the pieces fit together.

---

## 1. Primary Control Plane (this package) – **Python / FastAPI on Fly.io**

| Layer | Choice | Why |
|-------|--------|-----|
| Runtime | Python 3.12 | Stable, excellent async ecosystem |
| API framework | FastAPI | High performance, automatic OpenAPI, type-safe |
| ASGI server | Uvicorn | Production-grade ASGI |
| Config | pydantic-settings | Env + secrets, validated |
| Hosting | Fly.io | Global edge, simple machines, cheap scale-to-zero |
| Health | `/health` always 200 when process is up | Passes Fly smoke checks |

**This is what deploys today.**  
App name: `goodlife-gateway-fabric-vmbi4w`  
URL after deploy: `https://goodlife-gateway-fabric-vmbi4w.fly.dev`

### Core endpoints
- `GET /` – handshake / status
- `GET /health` – liveness (Fly + Docker healthcheck)
- `POST /api/v1/telemetry` – edge / simulation telemetry
- `POST /api/v1/contact` – lead / contact form
- `POST /api/v1/vbe/propose` + decide – Validation-Before-Execution gate

---

## 2. Optional Frontend Stack (Next.js) – recommended for public site & dashboards

If you want a marketing site, investor portal, Learning Lab UI, or authenticated dashboards:

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | Next.js 15 (App Router) | Server Components, streaming, edge-ready |
| Language | TypeScript | Type safety end-to-end |
| Styling | Tailwind CSS + design tokens | Fast, consistent UI |
| Auth | Auth.js (NextAuth) | Sessions, OAuth, role claims |
| ORM / DB | Prisma + PostgreSQL (Neon / Supabase / Fly Postgres) | Type-safe, migrations |
| Payments | Stripe (Checkout + Customer Portal + webhooks) | Subscriptions, trials, invoices |
| Email | Resend | Reliable transactional |
| Hosting | Vercel (primary) or Fly.io | Zero-config edge for frontend |

**Recommendation:** keep the **Python FastAPI service** as the control-plane / matrix / VBE / telemetry backend, and let Next.js call it via `NEXT_PUBLIC_API_URL` or internal service discovery.

```
┌─────────────────────┐         ┌──────────────────────────────┐
│  Next.js (Vercel)   │  HTTP   │  FastAPI Control Plane       │
│  Marketing + Auth   │ ──────► │  (Fly.io)                    │
│  Dashboard UI       │         │  /health /telemetry /vbe     │
└─────────────────────┘         └──────────────────────────────┘
         │                                      │
         ▼                                      ▼
   Prisma + Postgres                     Heartbeat / Audit logs
```

---

## 3. Database recommendations

| Use case | Recommendation |
|----------|----------------|
| Control-plane state (proposals, audit, telemetry) | Start with in-memory (current) → move to Redis or Postgres when multi-machine |
| User accounts, subscriptions, Learning Lab | PostgreSQL via Neon, Supabase, or Fly Postgres + Prisma |
| High-volume telemetry | Consider Timescale / ClickHouse later |

For a single Fly machine the current in-memory VBE store is fine. When you scale `min_machines_running > 1`, replace `_proposals` with Redis or Postgres.

---

## 4. Secrets & environment

Set on Fly (never commit real values):

```bash
fly secrets set \
  SECRET_KEY="$(openssl rand -hex 32)" \
  JWT_SECRET="$(openssl rand -hex 32)" \
  -a goodlife-gateway-fabric-vmbi4w
```

Optional later:
- `DATABASE_URL`
- `NVIDIA_API_KEY`
- SMTP / Resend credentials
- Stripe keys (on the Next.js side)

See `env.example`.

---

## 5. CI / CD

This package includes `.github/workflows/fly-deploy.yml`.

1. Add a GitHub secret: `FLY_API_TOKEN` (from `fly tokens create deploy`)
2. Push to `main` → automatic deploy

Or deploy manually:

```bash
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

---

## 6. Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Then:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/
pytest tests/ -v
```

---

## 7. Scaling & reliability tips

- Keep `min_machines_running = 0` for cost until traffic justifies always-on.
- Grace period of 25 s in `fly.toml` covers cold starts.
- Health endpoint returns 200 immediately so Fly smoke checks pass even before the orchestrator heartbeat is written.
- For multi-region later: add more regions in `fly.toml` and use Fly’s global proxy.

---

## 8. What NOT to mix in the same Docker image

Do **not** append a Node / Next.js stage to the Python Dockerfile.  
The final stage must remain pure Python + uvicorn.  
Frontend deploys separately (Vercel recommended).

---

## 9. Next engineering priorities (recommended order)

1. Deploy this package successfully → green `/health`
2. Wire real secrets + optional SMTP for contact form
3. Replace in-memory VBE store with Redis or Postgres when scaling
4. Stand up Next.js frontend that calls this API
5. Add Prisma schema for users / roles / subscriptions
6. Stripe Checkout + webhooks
7. NVIDIA / simulation integrations via telemetry endpoint

---

© 2026 Odynex Axis Logistics LLC. All rights reserved.
