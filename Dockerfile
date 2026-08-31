FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/opt/odynex-axis-matrix
ENV PORT=8080

WORKDIR /opt/odynex-axis-matrix

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        bash \
        ca-certificates \
        jq \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "omni_service:app", "--host", "0.0.0.0", "--port", "8080"]RUN python3 asset-defense/morpheus_security.py

# Default entry execution path targets your central system matrix baseline module
ENTRYPOINT ["python3", "core-kernel/deterministic_engine.py"]
