FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/opt/odynex-axis-matrix
ENV PORT=8080

WORKDIR /opt/odynex-axis-matrix

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "omni_service:app", "--host", "0.0.0.0", "--port", "8080"]
