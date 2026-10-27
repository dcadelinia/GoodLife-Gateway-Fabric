# NVIDIA Capital Connect – Technical Readiness Notes

**Project:** GoodLife Gateway Fabric (Project Koridor / Mycelium Edge Intelligence Stack)  
**Entity:** Odynex Axis Logistics LLC  
**Status:** Starter Kit control plane – Version 1.2  
**Operator:** David Fabian Cadelinia · Albany / SOWEGA, Georgia

## What this repository demonstrates

1. **Clear hybrid architecture** – Edge (Jetson) / Cloud control plane / Omniverse simulation.
2. **Governance-native design** – Validation Before Execution gate + immutable audit trail.
3. **Deployable control plane** – FastAPI, multi-stage Docker, Fly.io config, health checks.
4. **No secrets in source** – Environment template only; production secrets via Fly secrets.
5. **NVIDIA alignment** – Jetson, TensorRT, ROS 2, Omniverse/OpenUSD, CUDA hooks in architecture.

## What is intentionally Starter Kit scope

- In-memory VBE proposals (swap for durable store)
- File-backed audit log (swap for append-only / ledger)
- Single-tenant operator model (multi-tenant RBAC next)
- Simulation/telemetry loops are structural, not full physics

## Path to production

| Phase | Focus |
|-------|--------|
| Starter Kit (current) | Control plane, VBE, audit, health, deploy |
| Production | Durable audit, auth/RBAC, multi-tenant, real edge telemetry |
| Regional | Federation, Omniverse twins, BioNeMo-assisted modeling |

## Recommended diligence artifacts

- This repository (source + deploy path)
- Architecture diagram (`docs/ARCHITECTURE.md`)
- Investor / strategic proposal materials (shared under NDA)
- NVIDIA Inception membership confirmation

## Contact for technical evaluation

Under mutual NDA only.  
Operator: David Fabian Cadelinia · Odynex Axis Logistics LLC
