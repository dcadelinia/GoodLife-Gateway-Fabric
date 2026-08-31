FROM python:3.11-slim

WORKDIR /app

# Ensure local imports work reliably during container boot
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run directly through main.py where your app context is defined
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
