# Architecture – GoodLife Gateway Fabric

## Hybrid Model

- **Edge / Field**: Jetson Cycle Nodes, sensors, local TensorRT / ROS 2 inference. These push events and state to the cloud.
- **Cloud Control Plane (this repository)**: Multi-tenant gateway, Sophon intelligence cycle orchestration, Validation Before Execution gate, immutable audit trail, dashboards, and regional federation.
- **Heavy Simulation**: Omniverse / OpenUSD twins and advanced physics models run on NVIDIA cloud or dedicated GPU resources.

## Core Flows

1. Cycle Node registers and authenticates.
2. Telemetry and observations are ingested.
3. Sophon-style cycle (Sense → Understand → Simulate → Reason → Predict → Coordinate) runs under policy.
4. Any action that changes state requires Validation Before Execution.
5. Approved decisions are written to the immutable audit log and then executed.
6. Multi-tenant dashboards and regional federation consume the governed state.

## Design Principles

- Continuity over extraction
- Value remains with the originating place
- Human oversight on every material action
- Immutable record of decisions
- Zero-disturbance deployment preference
- Private-land and ratepayer-protection posture
