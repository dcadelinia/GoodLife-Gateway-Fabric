# GoodLife Gateway Fabric

**Premium multi-tenant SaaS platform**  
**Odynex Axis Logistics LLC** · NVIDIA Inception Program Member  
**Founder & Institutional Architect:** David Fabian Cadelinia  
Phone: 229-364-1658 · Email: david@odynexaxis.biz · Website: https://www.odynexaxis.biz

---

## Architecture Summary

This repository is a production-oriented foundation for a big-tech-quality SaaS product built with:

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Framework | Next.js 15 (App Router) + TypeScript | Server Components, streaming, edge-ready, excellent DX |
| Styling | Tailwind CSS + design tokens + dark/light | Enterprise polish, accessibility, responsive by default |
| Database | PostgreSQL + Prisma ORM | Type-safe, migrations, excellent relational modeling |
| Auth | NextAuth.js (Auth.js) + Prisma adapter | Secure sessions, OAuth-ready, role claims |
| Payments | Stripe (Checkout, Customer Portal, Webhooks) | Industry standard for subscriptions, trials, invoices |
| Email | Resend | Reliable transactional delivery |
| Validation | Zod | End-to-end type-safe schemas |
| Monitoring | Sentry-compatible hooks | Error tracking ready |
| Deployment | Vercel (primary) + Docker optional | Zero-config, global edge, managed Postgres |
| CI | GitHub Actions | Lint, typecheck, test, build on every PR |

**Module boundaries**
- `src/app` — routes (public marketing + authenticated dashboard)
- `src/components` — UI primitives, layout, marketing, dashboard, Learning Lab
- `src/lib` — auth, stripe, email, validations, utils
- `prisma` — schema + seed
- `docs` — architecture, compliance notes, deployment

**Roles implemented in schema**
Guest · Free · Student · Pro · Team Admin · Org Member · Instructor · Student Learner · Parent/Guardian · Institutional Admin · Platform Admin · Investor · Sponsor · Strategic Partner

**Pricing tiers (Stripe-ready)**
Free · Student/Learner · Pro · Team · Enterprise/Institutional (custom quote) · Sponsor

**Learning Lab**
Age-banded content groups (Future Technology Basics, AI Literacy, Logistics & Supply-Chain, Coding & Data, Entrepreneurship, Career Pathways, College & Professional Readiness). Parent/guardian consent workflow placeholders, educator portal concept, progress tracking, certificates framework. All youth-related flows flagged for legal review (COPPA / education-sector).

**Investor & Sponsor portals**
Role-restricted dashboards, request-access + admin approval, public “Investors & Partners” landing with legal disclaimer that nothing constitutes an offer to sell securities.

**Security baseline**
- Input validation (Zod)
- CSRF via NextAuth / SameSite
- Role checks on every protected server action / API
- Secure headers + CSP guidance
- Audit logging model
- GDPR/CCPA-friendly export/deletion framework
- WCAG 2.2 AA target

---

## Quick Start

```bash
# 1. Clone / extract this repository
cd goodlife-gateway-fabric

# 2. Install
npm install

# 3. Environment
cp .env.example .env.local
# Fill DATABASE_URL, NEXTAUTH_SECRET, Stripe keys, Resend key

# 4. Database
npx prisma generate
npx prisma db push
npm run db:seed   # optional demo data

# 5. Develop
npm run dev
# → http://localhost:3000
```

### Production build check
```bash
npm run typecheck
npm run lint
npm run build
```

---

## Stripe Configuration (Owner Action Required)

1. Create products & prices in Stripe Dashboard for:
   - Student monthly / yearly
   - Pro monthly / yearly
   - Team monthly / yearly (seat-based)
2. Copy Price IDs into `.env`
3. Add webhook endpoint: `https://your-domain.com/api/webhooks/stripe`
   Events: `checkout.session.completed`, `customer.subscription.*`, `invoice.*`
4. Set `STRIPE_WEBHOOK_SECRET`
5. Customer Portal: enable in Stripe Dashboard → Settings → Billing → Customer portal

**Trials**: configurable 7/14/30-day trials per tier. Card-required vs card-free controlled by env. Conversion handled by Stripe + webhook entitlement update.

**Enterprise / Institutional**: invoice-based / custom quote pathway (no fixed price ID). Contact form routes to founder.

---

## Deployment (Vercel + Managed Postgres)

1. Push repo to GitHub
2. Import project in Vercel
3. Add all environment variables from `.env.example`
4. Attach Neon / Supabase / Vercel Postgres
5. Deploy
6. Run `npx prisma migrate deploy` (or use Vercel build command that includes it)
7. Configure custom domain + Stripe webhook with production URL
8. Set up Resend domain verification
9. Optional: Sentry DSN

Docker support is optional; a production Dockerfile can be added later if self-hosting is required.

---

## Required Owner / Legal Actions Before Launch

- [ ] Stripe account + products + webhook + Customer Portal
- [ ] Resend (or SendGrid) domain authentication
- [ ] NEXTAUTH_SECRET rotation for production
- [ ] Professional legal review of:
  - Terms of Service, Privacy Policy, Cookie Notice, Refund Policy
  - Children’s data / COPPA / parental consent flows
  - Education-sector (FERPA-adjacent) data practices
  - Securities / investor solicitation disclaimers
  - Sponsorship contracts & promotional law
  - Referral / affiliate program terms
- [ ] Accessibility audit (WCAG 2.2 AA)
- [ ] Penetration / security review of auth + billing endpoints
- [ ] Data Processing Agreement with any sub-processors

---

## Production-Readiness Checklist

- [x] Clean folder structure & module boundaries
- [x] TypeScript strict + Prisma typed models
- [x] Design system tokens (light/dark)
- [x] Security headers + CSP baseline
- [x] Role model covering all specified roles
- [x] Subscription + trial + entitlement schema
- [x] Learning Lab course / lesson / progress model
- [x] Investor / Sponsor / Lead models
- [x] Audit log + consent records
- [x] `.env.example` with every required variable documented
- [x] Stripe webhook path documented
- [x] Database migrations via Prisma
- [x] CI-ready scripts (lint, typecheck, build)
- [ ] Full page implementations (Home, Platform, Solutions, Pricing, Learning Lab, About, Contact, Blog, FAQ, legal pages, auth flows, dashboard tabs)
- [ ] Stripe Checkout + Portal + webhook handlers fully wired
- [ ] Email templates + lifecycle sequences
- [ ] Unit + integration tests for billing entitlement
- [ ] E2E journeys
- [ ] Seed data for Learning Lab curriculum
- [ ] Admin RBAC guards on every protected action

**Next engineering steps (priority order)**
1. Implement `src/lib/auth` + NextAuth config + role guards
2. Implement Stripe webhook + checkout session creators
3. Build marketing pages (Home → Contact) with shared layout & navigation
4. Build authenticated dashboard shells + entitlement checks
5. Seed Learning Lab content + parent consent placeholders
6. Investor / Sponsor request-access flows
7. CI workflow + health endpoint
8. Full test suite

---

## Contact

**David Fabian Cadelinia**  
Founder & Institutional Architect  
Odynex Axis Logistics LLC  
NVIDIA Inception Program Member  
Phone: 229-364-1658  
Email: david@odynexaxis.biz  
Website: https://www.odynexaxis.biz

---

© 2026 Odynex Axis Logistics LLC. All rights reserved.  
This repository is proprietary. Unauthorized distribution prohibited.
