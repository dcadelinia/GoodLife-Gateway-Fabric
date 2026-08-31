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

# Run your mandatory framework validation check during compilation
RUN python3 asset-defense/morpheus_security.py

# Default entry execution path targets your central system matrix baseline module
ENTRYPOINT ["python3", "core-kernel/deterministic_engine.py"]
