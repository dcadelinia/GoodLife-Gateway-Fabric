# Use a slim, stable base Python image
FROM python:3.11-slim

# Force root directory bounds inside the container
WORKDIR /app

# Ensure Python looks inside /app so your custom modules import flawlessly
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install dependencies cleanly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all core files, YAML blueprints, and project directories into the image
COPY . .

# EXPOSE port 8080 to match your fly.toml configuration
EXPOSE 8080

# TARGETS YOUR TRUE APPLICATION MODULE
CMD ["uvicorn", "omni_service:app", "--host", "0.0.0.0", "--port", "8080"]
