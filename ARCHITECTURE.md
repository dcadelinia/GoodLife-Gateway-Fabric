# Architecture — GoodLife Gateway Fabric

## System Context

Odynex Axis Logistics LLC provides a multi-tenant SaaS control plane that combines:

1. Subscription & entitlement management (Stripe)
2. Role-based access for learners, educators, parents, institutions, investors, sponsors
3. Learning Lab content delivery with age-appropriate pathways
4. CRM / lead capture for enterprise, investor, and sponsor pipelines
5. Audit logging and consent tracking for compliance posture

## Key Decisions

- **Next.js App Router** chosen for server-first rendering, streaming, and unified frontend/backend.
- **Prisma + PostgreSQL** for relational integrity across users, orgs, subscriptions, courses, and audit.
- **NextAuth** for session security; roles stored on User and checked in server actions / middleware.
- **Stripe** for all paid flows; entitlements derived from subscription status, never client claims.
- **No live payment processing** until owner configures Stripe keys and products.
- Youth / education data flows are scaffolded with consent models but require legal review before any production use involving minors.

## Future Edge Integration

The original GoodLife-Gateway-Fabric Python control plane (Möbius loop, Validation-Before-Execution, Jetson edge nodes) can be attached as a separate microservice or edge gateway. This SaaS layer is the human-facing product surface and billing authority.
