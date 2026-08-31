Hi, I'm trying to fix my Fly.io deployment. There's a build error on my Dockerfile.

Please fix my Dockerfile for me to the best of your ability. And give me the updated version so I can paste in Fly.io web deployment UI.

Error logs:

```
flyctl deploy --build-only --push -a goodlife-gateway-fabric --image-label deployment-3d0a707fd1b5ae678ab451a2d3f66347 --config fly.toml
==> Verifying app config
--> Verified app config
Validating fly.toml
[32m✓[0m Configuration is valid
==> Building image
Waiting for remote builder fly-builder-tranquil-valley-1715...

Remote builder fly-builder-tranquil-valley-1715 ready
[33mWARN[0m The running flyctl agent (v2026.8.31-dev.1788155998) is older than the current flyctl (v2026.8.31-dev.1788155997).
[33mWARN[0m The out-of-date agent will be shut down along with existing wireguard connections. The new agent will start automatically as needed.
[32m==> Building image with Buildpacks[0m
[38;5;252m--> docker host: 24.0.7 linux x86_64[0m
==> Building image
👀 checking remote builder compatibility with wireguardless deploys ...
✓ compatible remote builder found
Waiting for remote builder fly-builder-tranquil-valley-1715...

[2mINFO[0m Override builder host with: https://fly-builder-tranquil-valley-1715.fly.dev (was tcp://[fdaa:bf:b97a:a7b:661:443a:6ec0:2]:2375)

Remote builder fly-builder-tranquil-valley-1715 ready
[32m==> Building image with Buildpacks[0m
[38;5;252m--> docker host: 24.0.7 linux x86_64[0m
Error: failed to fetch an image or build from source: failed to fetch builder image 'index.docker.io/library/none:latest': failed to connect to the docker API at unix:///var/run/docker.sock: lookup /var/run/docker.sock: no such host
Dockerfile failed to build error
unsuccessful command 'flyctl deploy --build-only --push -a goodlife-gateway-fabric --image-label deployment-3d0a707fd1b5ae678ab451a2d3f66347 --config fly.toml'
```

Dockerfile


```
# Optimized for Fly.io CPU deployment compatibility
FROM python:3.11-slim

# Prevent interactive prompts during software package provisioning
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install basic environment dependencies and core runtime tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    bash \
    ca-certificates \
    jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the internal application directory within the container
WORKDIR /opt/odynex-axis-matrix

# Copy all validated repository framework modules and data configurations
COPY . .

# Update pip setup inside the runtime layer
RUN pip3 install --no-cache-dir --upgrade pip setuptools

# Set runtime workspace environments to look for core execution kernels
ENV PYTHONPATH=/opt/odynex-axis-matrix

# Keeps the container up and running smoothly on standard cloud nodes
CMD ["tail", "-f", "/dev/null"]
RUN python3 asset-defense/morpheus_security.py

# Default entry execution path targets your central system matrix baseline module
ENTRYPOINT ["python3", "core-kernel/deterministic_engine.py"]

```


fly.toml


```
# fly.toml app configuration file generated for goodlife-gateway-fabric on 2026-08-31T05:59:52Z
#
# See https://fly.io/docs/reference/configuration/ for information about how to use this file.
#

app = 'goodlife-gateway-fabric'
primary_region = 'syd'

[build]
  builder = 'none'

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = 'stop'
  auto_start_machines = true
  min_machines_running = 0
  processes = ['app']

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1
  memory_mb = 1024

```

