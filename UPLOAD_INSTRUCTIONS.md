# How to upload this package to the GitHub repository

This folder is a **clean, complete, Capital-Connect-ready** control plane for  
`https://github.com/dcadelinia/GoodLife-Gateway-Fabric`.

## Important security note

The existing public repository contains a file (`omni_service.py`) with a **hardcoded SMTP password**.  
Do **not** keep that file. This package replaces the insecure entrypoint with a proper `app/` structure.

### Recommended upload method

1. **Backup** the current repo (or create a branch `legacy-backup`).
2. **Make the repository private** if the proprietary notice is binding.
3. Clone or pull the repo locally.
4. **Remove** or archive sensitive/legacy items:
   - `omni_service.py` (hardcoded credentials)
   - Root-level PDFs / pitch decks (move to private storage under NDA)
   - Old duplicate deploy workflows if they conflict
5. Copy the contents of this zip **into** the repository root (merge carefully).
6. `cp env.example .env` and set real secrets only in Fly / local `.env`.
7. Commit and push:

```bash
git add app/ config/ system_config/ docs/ tests/ scripts/ \
        Dockerfile fly.toml requirements.txt env.example \
        README.md LICENSE .gitignore .dockerignore \
        .github/workflows/ci.yml .github/workflows/fly-deploy.yml
git status   # review – ensure no secrets
git commit -m "Complete control plane for Capital Connect: secure app structure, VBE gate, audit, deploy"
git push origin main
```

8. Set Fly secrets:

```bash
fly secrets set JWT_SECRET="..." SECRET_KEY="..."
# optional: SMTP_*, NVIDIA_API_KEY, etc.
fly deploy
```

9. Enable GitHub Actions secrets: `FLY_API_TOKEN` if using the deploy workflow.

## What this package includes

- Complete README with structure + quick start
- Secure FastAPI app (`app.main:app`) matching the Dockerfile
- Validation Before Execution (VBE) gate + immutable audit trail
- Health endpoints for Fly.io
- Multi-stage Dockerfile (non-root user)
- `fly.toml`, CI + deploy workflows
- Tests, architecture & Capital Connect docs
- LICENSE (proprietary)
- No secrets, no hardcoded passwords

## What it intentionally does NOT include

- Large pitch PDFs (keep under NDA storage)
- Hardcoded credentials
- Full multi-tenant production auth (documented as next phase)
