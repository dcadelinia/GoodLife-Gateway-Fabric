# Fix Dockerfile NOW (copy-paste)

## Problem
Your GitHub `Dockerfile` ends with a second stage:

```
FROM node:20-alpine AS runner
COPY --from=builder /app/.next/standalone ./
...
CMD ["node", "server.js"]
```

Docker builds the **last** stage → build fails.

## Fix (on the machine where you run fly deploy)

```bash
# 1. Open the repo
cd /path/to/GoodLife-Gateway-Fabric

# 2. Replace Dockerfile entirely with the pure-Python version
#    (use the Dockerfile.FIXED contents – must END at the uvicorn CMD)

# 3. Ensure app package exists
ls app/main.py || echo "MISSING app/ – unzip goodlife-gateway-BUILD-FIX.zip first"

# 4. Verify Dockerfile has NO node:20-alpine and NO .next
grep -n "node:20\|.next\|server.js" Dockerfile && echo "STILL BROKEN" || echo "Dockerfile OK"

# 5. Commit and push
git add Dockerfile app/
git commit -m "fix: remove appended Node stage; pure Python final image"
git push origin main

# 6. Deploy from this directory
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

Or overwrite in place from the fixed file:

```bash
# After downloading Dockerfile.FIXED
cp Dockerfile.FIXED Dockerfile
grep -c "FROM " Dockerfile   # should print 2 (builder + runtime only)
fly deploy -a goodlife-gateway-fabric-vmbi4w
```

## Checklist before fly deploy
- [ ] `Dockerfile` has exactly **two** `FROM` lines (both python:3.12-slim)
- [ ] No `node:20-alpine`
- [ ] No `COPY ... .next`
- [ ] No `CMD ["node", "server.js"]`
- [ ] Last line is `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]`
- [ ] `app/main.py` exists in the build context
