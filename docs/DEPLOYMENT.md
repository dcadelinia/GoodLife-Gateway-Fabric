# Deployment Guide – Fly.io

## Prerequisites
- Fly.io account
- flyctl installed and authenticated
- Docker

## First-time setup

```bash
fly launch --no-deploy
fly postgres create --name odynex-db --region iad
fly postgres attach odynex-db
fly secrets set JWT_SECRET=$(openssl rand -hex 32)
fly deploy
