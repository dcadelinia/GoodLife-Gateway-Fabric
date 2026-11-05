# One-Command Deploy Guide – GoodLife Gateway Fabric

## Prerequisites

- [flyctl](https://fly.io/docs/hands-on/install-flyctl/) installed
- Logged in: `fly auth login`
- App already exists: `goodlife-gateway-fabric-vmbi4w`

---

## Fast path (recommended)

```bash
# From the directory that contains this package (after unzip)
cd goodlife-complete-fix   # or whatever you named the folder

# Optional but recommended
fly secrets set \
  SECRET_KEY="$(openssl rand -hex 32)" \
  JWT_SECRET="$(openssl rand -hex 32)" \
  -a goodlife-gateway-fabric-vmbi4w

# Build + deploy
fly deploy -a goodlife-gateway-fabric-vmbi4w

# Verify
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/health | jq
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/ | jq
fly status -a goodlife-gateway-fabric-vmbi4w
```

---

## What this package fixes

| Problem | Fix |
|---------|-----|
| `requirements.txt` contained markdown / ```bash | Replaced with pure pip dependencies |
| Missing `app/` package → ModuleNotFoundError | Full `app/` tree with main, api, core, services |
| Health checks failing on cold start | `/health` always returns 200 when process is alive |
| Possible Node stage in Dockerfile | Pure Python multi-stage only |
| Weak health check timing | 25 s grace period + Docker HEALTHCHECK |

---

## If deploy still fails

```bash
# See live logs
fly logs -a goodlife-gateway-fabric-vmbi4w

# List machines
fly machines list -a goodlife-gateway-fabric-vmbi4w

# Force destroy a stuck machine (last resort)
fly machines destroy <MACHINE_ID> --force

# Redeploy
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

---

## Local smoke test (before pushing)

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
# another terminal
curl http://localhost:8080/health
pytest tests/ -v
```

---

## GitHub Actions

After you push this tree to `main` and add the secret `FLY_API_TOKEN`,  
every push to `main` will deploy automatically via `.github/workflows/fly-deploy.yml`.

Create the token:

```bash
fly tokens create deploy -a goodlife-gateway-fabric-vmbi4w
```

Add it in GitHub → Settings → Secrets → Actions → `FLY_API_TOKEN`.

---

## Success criteria

- `fly status` shows the machine running
- `curl …/health` returns `"status": "HEALTHY"`
- `curl …/` returns `"status": "ONLINE"`
- No more `Invalid requirement: '```bash'` build errors
