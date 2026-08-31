# Optimized light-weight base image for multi-agent architecture execution
FROM python:3.11-slim

# Enforce explicit application directory scope
WORKDIR /app

# Optimize Python execution constraints for real-time inference handling
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install systemic hardware-agnostic baseline dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all logical configuration layers into container namespace
COPY . .

# CRITICAL FIX: Direct Uvicorn to target the explicit spatial routing file
CMD ["uvicorn", "gateway_router:app", "--host", "0.0.0.0", "--port", "8080"]
