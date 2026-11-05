# Live Fix – goodlife-gateway-fabric-vmbi4w.fly.dev

## Why the site never finished loading

1. Dockerfile runs `uvicorn app.main:app`
2. GitHub repo had **no `app/` Python package**
3. Process crashed on every start → Fly proxy got no response → browser spun forever
4. `min_machines_running = 0` + crash loop made cold starts hang

## What this package fixes

- Complete `app/` package (`main`, health, contact, telemetry, VBE, orchestrator)
- `/health` always returns **200** when the process is alive
- Dockerfile binds `0.0.0.0:8080`
- `fly.toml` sets `min_machines_running = 1` and a 30s health-check grace period
- No hardcoded secrets (use `fly secrets`)

## Deploy now

```bash
# From the root of this extracted folder (or merge into your repo root)
# 1. Push to GitHub (recommended) OR deploy from local directory

fly secrets set SECRET_KEY="$(openssl rand -hex 32)" JWT_SECRET="$(openssl rand -hex 32)" -a goodlife-gateway-fabric-vmbi4w

fly deploy -a goodlife-gateway-fabric-vmbi4w

# Verify
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/health
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/
fly status -a goodlife-gateway-fabric-vmbi4w
fly logs -a goodlife-gateway-fabric-vmbi4w
```

If machines are stuck from previous crash loops:

```bash
fly machines list -a goodlife-gateway-fabric-vmbi4w
fly machines destroy <id> --force   # only failed ones
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

## Local test

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/
```

## Security note

Do **not** commit SMTP passwords or API keys. The old `omni_service.py` on GitHub contained a plaintext password — rotate that credential and use environment variables / Fly secrets only.

Odynex Axis Logistics LLC · NVIDIA Inception  
David Fabian Cadelinia · david@odynexaxis.biz · 229-364-1658
