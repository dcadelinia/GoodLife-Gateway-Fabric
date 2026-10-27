<!-- ======================================================================= -->
<!--                   PROPRIETARY & CONFIDENTIALITY NOTICE                  -->
<!-- ======================================================================= -->
⚠️ **PROPRIETARY & CONFIDENTIAL INFORMATION**

THIS REPOSITORY AND ALL ASSOCIATED SOURCE CODE, DATA MATRICES, OPENUSD BLUEPRINTS,  
AND LOGICAL CONFIGURATIONS ARE THE EXCLUSIVE INTELLECTUAL PROPERTY OF **ODYNEX AXIS  
LOGISTICS LLC**, MANAGED UNDER THE DIRECT STEWARDSHIP OF OPERATOR DAVID FABIAN CADELINIA.

ACCESS IS RESTRICTED TO AUTHORIZED ENTERPRISE EVALUATORS (INCLUDING NVIDIA INCEPTION  
CAPITAL CONNECT AND QUALIFIED STRATEGIC PARTNERS) UNDER MUTUAL NDA.

UNAUTHORIZED COPYING, DISTRIBUTION, OR DERIVATIVE USE IS STRICTLY PROHIBITED.  
Core logical configurations and spatial algorithms are protected by publicly recorded  
prior-art timestamps (Lulu Marketplace ID: M2EPZ6R and related Amazon KDP filings).
<!-- ======================================================================= -->

# GoodLife Gateway Fabric

### Continuous Möbius Loop Architecture for Living Systems & Regional Infrastructure

**Odynex Axis Logistics LLC** · NVIDIA Inception Member · Albany, Georgia · SOWEGA  
**Compliance-Ready Architecture | Version 1.2** · Ready for NVIDIA Capital Connect

---

## Overview

The **GoodLife Gateway Fabric** (also referred to as Project Koridor / Mycelium Edge Intelligence Stack) is the cloud control plane and coordination layer for Odynex’s Living Matrix platform.

It turns fragmented monitoring of flora, soil, water, and wildlife into a continuous, human-supervised, auditable system that keeps value inside the originating region.

**Core differentiators (aligned with the Investor & Strategic Partner Proposal):**

- Continuity over extraction
- Full living-cycle coupling (Botanical + Soil/Hydrological + Wildlife)
- Zero-disturbance modular deployment on existing pads and corridors
- Governance-native: human-supervised **Validation Before Execution** gates + immutable audit logs
- Private-land focus, ratepayer-protection modeling, non-advisory posture

## Hybrid Architecture

| Layer | Responsibility | Runtime |
|-------|----------------|---------|
| **Edge / Field** | Jetson-based Cycle Nodes, sensors, local inference, ROS 2 | Physical Jetson / on-prem |
| **Cloud Control Plane** *(this repository)* | Multi-tenant gateway, Sophon intelligence cycle orchestration, Validation Before Execution gate, immutable audit trail, multi-tenant dashboards, federation | Fly.io (primary), container platforms |
| **Heavy Simulation / Digital Twins** | Omniverse / OpenUSD collaborative twins, advanced physics, BioNeMo-assisted modeling | NVIDIA cloud / dedicated GPU resources |

This separation is required for reliable cloud deployment and matches the **Starter Kit → Production → Regional** path in the proposal.

## Key Capabilities (Current Focus)

- Continuous multi-use IP fabric with Möbius-loop routing concepts
- Protective coordination layer for living cycles
- Human-supervised decision gates (Validation Before Execution / JusticeTree-style)
- Immutable audit trail of spatial, financial, and decision data
- Multi-tenant Starter Kit support and path to regional federation
- Compliance-oriented controls (AI governance, consent, purpose limitation, data sovereignty)

## NVIDIA Inception & Capital Connect Alignment

Architecture is designed from the start for:

- Jetson Edge AI (vision, TensorRT, ROS 2 nodes)
- Omniverse + OpenUSD digital twins
- CUDA / physics-informed modeling hooks
- Human oversight, bias screening, and immutable logs consistent with responsible AI expectations
- Clear separation of control plane vs. edge vs. simulation for investor technical due diligence

## Repository Structure

```
GoodLife-Gateway-Fabric/
├── app/                          # FastAPI application (primary entrypoint)
│   ├── main.py                   # Application factory + health endpoints
│   ├── api/                      # HTTP routes
│   ├── core/                     # Config, security, audit, VBE gate
│   ├── models/                   # Pydantic schemas
│   └── services/                 # Business logic (orchestrator, telemetry)
├── config/                       # Runtime configuration templates
├── system_config/                # Gateway manifest & node definitions
├── docs/                         # Architecture, compliance, Capital Connect notes
├── scripts/                      # Local helpers & verification
├── tests/                        # Smoke & unit tests
├── .github/workflows/            # CI + Fly.io deploy
├── Dockerfile                    # Multi-stage production image
├── fly.toml                      # Fly.io deployment config
├── requirements.txt              # Pinned dependencies
├── env.example                   # Environment variable template (no secrets)
└── README.md
```

## Quick Start (Local Development)

### Prerequisites

- Python 3.11 or 3.12
- Docker (optional, for container runs)
- Fly.io CLI (`fly`) for production deploy

### 1. Clone & configure

```bash
git clone https://github.com/dcadelinia/GoodLife-Gateway-Fabric.git
cd GoodLife-Gateway-Fabric

cp env.example .env
# Edit .env — never commit real secrets
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the gateway locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Open:

- Health: http://localhost:8080/health
- Root status: http://localhost:8080/
- Interactive docs: http://localhost:8080/docs

### 4. Run tests

```bash
pytest tests/ -v
```

## Deployment (Fly.io)

```bash
# First time
fly launch --copy-config --no-deploy   # review fly.toml
fly secrets set JWT_SECRET="..." SECRET_KEY="..."   # set real values

# Deploy
fly deploy
```

Health checks hit `/health`. The service listens on port **8080**.

## Validation Before Execution (VBE) Gate

Critical control actions pass through a human-supervised gate before execution.  
See `app/core/vbe_gate.py` and `docs/ARCHITECTURE.md`.

Audit events are written to an immutable log stream (currently file-backed for Starter Kit; replaceable with append-only store or ledger in production).

## Security Notes

- **Never** commit real credentials, SMTP passwords, or API keys.
- All secrets must live in environment variables or Fly secrets.
- CORS, JWT, and rate-limiting hooks are present and configurable.
- The previous root-level `omni_service.py` contained hardcoded credentials and has been superseded by the secure `app/` structure.

## Capital Connect Readiness Checklist

- [x] Clear hybrid architecture (Edge / Cloud / Omniverse)
- [x] Working FastAPI control plane with health endpoints
- [x] Validation Before Execution gate stub + audit trail
- [x] Multi-stage Dockerfile + Fly.io config
- [x] Environment template without secrets
- [x] CI workflow skeleton
- [x] Documentation suitable for technical due diligence
- [ ] Production database / append-only audit store (next phase)
- [ ] Full multi-tenant auth + RBAC (next phase)
- [ ] Omniverse / OpenUSD integration hooks (simulation layer)

## Related Odynex Repositories

- Transactional Core Engine
- JetWay Core Engine (simulation)
- Project Bilis / other domain modules

## License & Access

Proprietary — Odynex Axis Logistics LLC.  
Evaluation access for NVIDIA Inception Capital Connect and NDA-covered strategic partners only.

---

**Operator:** David Fabian Cadelinia · Odynex Axis Logistics LLC · Albany / SOWEGA, Georgia  
**NVIDIA Inception Member**
