# Security Notes

## Critical rules

1. **Never commit secrets.** Use `env.example` only. Real values go in `.env` (gitignored) or Fly secrets.
2. The previous `omni_service.py` in the legacy tree contained a hardcoded SMTP password. That file is **not** included in this complete package. Do not restore it.
3. Rotate any credentials that may have been exposed in public history.

## Production checklist

- [ ] Set strong `JWT_SECRET` and `SECRET_KEY` via Fly secrets
- [ ] Restrict `CORS_ORIGINS` to known frontends
- [ ] Disable `/docs` in production (already controlled by ENVIRONMENT)
- [ ] Use private repository for full IP if required by NDA posture
- [ ] Enable Dependabot / secret scanning on GitHub
- [ ] Review audit log retention and access controls
