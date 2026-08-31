FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# TARGETS YOUR TRUE APPLICATION MODULE
CMD ["uvicorn", "omni_service:app", "--host", "0.0.0.0", "--port", "8080"]
