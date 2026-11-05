# Dockerfile Build Fix

## Error you hit

```
COPY --from=builder /app/.next/standalone ./
ERROR: ... /app/.next: no such file or directory
```

The Dockerfile on the branch is a **broken hybrid**:
- Stage 1 = Python (installs requirements.txt)
- Stage 2 = Node Alpine, then tries to copy `.next/standalone`, `.next/static`, `public/`

Those Next.js artifacts were never built, so the image build fails.

## Fix

Replace the repo root `Dockerfile` (and preferably `fly.toml` + `.dockerignore`) with the pure-Python versions in this zip.

**Required:** the `app/` package must exist in the build context (from the previous LIVE-FIX package):

```
app/
  main.py
  api/health.py
  ...
requirements.txt
Dockerfile   ← this one
fly.toml
```

## Deploy

```bash
# Ensure app/ package is present
ls app/main.py

# Replace Dockerfile (and fly.toml)
cp Dockerfile /path/to/repo/
cp fly.toml /path/to/repo/
cp .dockerignore /path/to/repo/

cd /path/to/repo
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

Or build-only first:

```bash
flyctl deploy --build-only --push -a goodlife-gateway-fabric-vmbi4w --config fly.toml
```

## Do not mix Next.js into this Dockerfile yet

Serving Next.js on the same Fly app requires either:
1. A proper multi-stage Dockerfile that runs `npm ci && npm run build` and then starts `node server.js`, or
2. A separate Fly app for the frontend.

Until the Python control plane is healthy and `/health` returns 200, keep this Dockerfile Python-only.

Odynex Axis Logistics LLC · NVIDIA Inception
