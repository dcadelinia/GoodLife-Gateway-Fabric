# GoodLife Gateway Fabric – Architecture

## Hybrid Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Heavy Simulation / Digital Twins                           │
│  Omniverse · OpenUSD · BioNeMo · CUDA physics               │
│  (NVIDIA cloud / dedicated GPU)                             │
└──────────────────────────▲──────────────────────────────────┘
                           │ twins / policies
┌──────────────────────────┴──────────────────────────────────┐
│  Cloud Control Plane  ← THIS REPOSITORY                     │
│  FastAPI gateway · VBE gate · Audit trail · Orchestrator    │
│  Multi-tenant · Federation path · Fly.io                    │
└──────────────────────────▲──────────────────────────────────┘
                           │ telemetry / commands
┌──────────────────────────┴──────────────────────────────────┐
│  Edge / Field                                               │
│  Jetson Cycle Nodes · ROS 2 · TensorRT · sensors            │
│  Local inference · safe-state loops                         │
└─────────────────────────────────────────────────────────────┘
```

## Validation Before Execution (VBE)

High-impact actions (route changes, node isolation, policy updates, firmware)  
must be proposed, human-approved, then executed. Every step is audited.

Endpoints:

- `POST /api/v1/vbe/propose`
- `POST /api/v1/vbe/{id}/decide`
- `GET  /api/v1/vbe/pending`

## Audit Trail

Append-only JSONL file in Starter Kit (`logs/audit/audit_events.jsonl`).  
Replace with durable append-only store or ledger for production.

## Health & Deployment

- `GET /health` (and `/healthz`) – used by Docker HEALTHCHECK and Fly.io
- Listens on port 8080
- Multi-stage Dockerfile, non-root user `odynex`

## Security Posture for Capital Connect

- No hardcoded credentials
- Secrets via environment / Fly secrets
- CORS configurable
- Human-in-the-loop for control actions
- Immutable audit of decisions
