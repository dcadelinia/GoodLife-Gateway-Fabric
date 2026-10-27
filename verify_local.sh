#!/usr/bin/env bash
# Local verification script – run before push / Capital Connect demos
set -euo pipefail

echo "==> Installing dependencies (if needed)"
pip install -q -r requirements.txt

echo "==> Import check"
python -c "from app.main import app; print('  app import OK')"

echo "==> Running tests"
pytest tests/ -v --tb=short

echo "==> Starting server for health check (background)"
uvicorn app.main:app --host 127.0.0.1 --port 18080 &
PID=$!
sleep 3

echo "==> Health check"
curl -sf http://127.0.0.1:18080/health || curl -sf http://127.0.0.1:18080/ || true
echo
curl -sf http://127.0.0.1:18080/ | head -c 200
echo

kill $PID 2>/dev/null || true
echo "==> Verification complete"
