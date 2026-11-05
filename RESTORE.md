# Restore deploy (read this)

## What broke the build
Someone appended a Node/Next.js stage to the end of Dockerfile.
Docker uses the LAST stage → it looks for .next files that do not exist → build fails.

## What this package does
- Replaces Dockerfile with pure Python only (no Node, no .next)
- Adds the missing app/ package so `uvicorn app.main:app` works
- Updates fly.toml health check

## Steps (copy-paste)

```bash
# From your machine, in a clean clone or your existing repo:
cd GoodLife-Gateway-Fabric

# Backup current broken Dockerfile
cp Dockerfile Dockerfile.BROKEN.bak

# Extract THIS package on top of the repo root
unzip -o /path/to/RESTORE-DEPLOY.zip

# Verify Dockerfile is clean
grep -c "^FROM " Dockerfile        # must be 2
grep -E "node:20|\.next|server.js" Dockerfile && echo FAIL || echo OK
ls app/main.py                     # must exist

# Commit and push
git add Dockerfile fly.toml requirements.txt .dockerignore app/
git commit -m "restore: pure Python image + app package so deploy builds again"
git push origin main

# Deploy
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

If deploy still uses a local broken file, force the path:

```bash
fly deploy -a goodlife-gateway-fabric-vmbi4w --dockerfile ./Dockerfile
```

## After deploy
```bash
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/health
curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/
```
