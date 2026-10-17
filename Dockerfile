# Entorno reproducible: la misma imagen corre en DEV, QA y PROD
FROM python:3.13-slim

WORKDIR /app

# 1. Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Codigo del proyecto
COPY src/ src/
COPY scripts/ scripts/
COPY config/ config/

# 3. El entorno se elige con una variable, no cambiando el codigo
ENV APP_ENV=dev

CMD ["python", "-m", "src.train_ventas"]