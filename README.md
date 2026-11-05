# GoodLife Gateway Fabric — SaaS Implementation

**Odynex Axis Logistics LLC** · NVIDIA Inception · David Fabian Cadelinia · david@odynexaxis.biz · 229-364-1658

## What's included

| Area | Status |
|------|--------|
| Marketing pages (Home, Platform, Solutions, Pricing, Learning Lab, About, Contact, Blog, FAQ, legal, Investors) | Implemented |
| Auth flows (Sign in, Sign up, Forgot password, Verify) | Implemented (Credentials; add OAuth as needed) |
| Dashboard tabs + RBAC guards (admin / investor / sponsor) | Implemented |
| Stripe Checkout + Customer Portal + Webhook entitlement updates | Implemented (requires Stripe env) |
| Email templates (welcome, trial, payment) | Scaffold (wire Resend) |
| Learning Lab seed curriculum | `prisma/seed.ts` |
| Unit tests for entitlements | `tests/unit` |
| CI workflow | `.github/workflows/ci.yml` |
| Health endpoint | `/api/health` |

## Quick start

```bash
npm install
cp .env.example .env.local
# Set DATABASE_URL, NEXTAUTH_SECRET, Stripe keys, Resend key
npx prisma db push
npm run db:seed
npm run dev
```

## Stripe

1. Create products/prices in Stripe Dashboard  
2. Set `STRIPE_PRICE_*` env vars  
3. Webhook: `POST /api/stripe/webhook` — events: `checkout.session.completed`, `customer.subscription.*`, `invoice.payment_failed`  
4. Enable Customer Portal in Stripe settings  

**Payment processing is not live until keys and price IDs are set.**

## Legal

Youth/COPPA, education data, securities/investor materials, sponsorship contracts, and marketing consent require professional legal review before launch.

## Deploy (Vercel recommended for this Next.js app)

```bash
# Vercel + managed Postgres
vercel
# Set env vars, run migrations, configure Stripe webhook to production URL
```

The Fly.io Python control plane is a separate service; this package is the SaaS product surface.
