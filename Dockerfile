# Location: odynex-axis-matrix/Dockerfile
# Architecture: Odynex Axis Logistics LLC — Automated Runtime Stack
# Base Platform: NVIDIA CUDA Linux Minimal Compute Environment

FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

# Prevent interactive prompts during software package provisioning
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install basic environment dependencies and Python 3.11 environment binaries
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3.11-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the internal application directory within the container
WORKDIR /opt/odynex-axis-matrix

# Copy all validated repository framework modules and data configurations
COPY core-kernel/ ./core-kernel/
COPY asset-defense/ ./asset-defense/

# Install python dependencies (Simulated environment targets for cuQuantum/Morpheus)
# Note: In active production, place standard tracking dependencies inside a requirements.txt file
RUN pip3 install --no-cache-dir --upgrade pip setuptools

# Set runtime workspace environments to look for core execution kernels
ENV PYTHONPATH=/opt/odynex-axis-matrix

# Execute automated framework unit checks upon launching the container to guarantee 0 errors
RUN python3 core-kernel/deterministic_engine.py
RUN python3 asset-defense/morpheus_security.py

# Default entry execution path targets your central system matrix baseline module
ENTRYPOINT ["python3", "core-kernel/deterministic_engine.py"]
