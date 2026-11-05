# Pre-Deploy & Post-Deploy Checklist

## Before `fly deploy`

- [ ] Unzipped this package into a clean directory
- [ ] `ls Dockerfile fly.toml requirements.txt app/main.py` all exist
- [ ] `grep -c "FROM " Dockerfile` shows **exactly 2** (builder + runtime)
- [ ] No `node:20` or `.next` anywhere in Dockerfile
- [ ] Last line of Dockerfile is the uvicorn CMD
- [ ] `requirements.txt` contains only package names (no markdown)
- [ ] Secrets set (or will be set): `SECRET_KEY`, `JWT_SECRET`

## After `fly deploy`

- [ ] `fly status -a goodlife-gateway-fabric-vmbi4w` shows started machine
- [ ] `curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/health` → 200 + `"HEALTHY"`
- [ ] `curl -s https://goodlife-gateway-fabric-vmbi4w.fly.dev/` → `"ONLINE"`
- [ ] `fly logs` shows no import / ModuleNotFoundError
- [ ] Optional: GitHub Actions workflow secret `FLY_API_TOKEN` configured

## Optional next steps

- [ ] Add real SMTP / Resend for contact form
- [ ] Move VBE store from memory → Redis or Postgres
- [ ] Stand up Next.js frontend (see STACK_RECOMMENDATIONS.md)
- [ ] Add custom domain on Fly
- [ ] Enable more regions when traffic grows
