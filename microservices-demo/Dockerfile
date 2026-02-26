# --- Base image ------------------------------------------------------
FROM python:3.11-slim AS base

# Install build‑time deps for psycopg2 (PostgreSQL driver) **before**
# dropping to a non‑root user.
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Add a non‑root user – do this *after* the apt‑get step.
RUN useradd -ms /bin/bash app
WORKDIR /app
USER app

# ---------------------------------------------------------------

# Build targets ---------------------------------------------------------
# User service
FROM base AS user
COPY --chown=app:app user_service/ ./user_service/
WORKDIR /app/user_service
RUN pip install --no-cache-dir -r requirements.txt

# Inventory service
FROM base AS inventory
COPY --chown=app:app inventory_service/ ./inventory_service/
WORKDIR /app/inventory_service
RUN pip install --no-cache-dir -r requirements.txt

# Order service
FROM base AS order
COPY --chown=app:app order_service/ ./order_service/
WORKDIR /app/order_service
RUN pip install --no-cache-dir -r requirements.txt

# API Gateway
FROM base AS gateway
COPY --chown=app:app api_gateway/ ./api_gateway/
WORKDIR /app/api_gateway
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------

# Final images ---------------------------------------------------------
FROM user AS user_image
ENTRYPOINT ["python", "-m", "user_service.app"]

FROM inventory AS inventory_image
ENTRYPOINT ["python", "-m", "inventory_service.app"]

FROM order AS order_image
ENTRYPOINT ["python", "-m", "order_service.app"]

FROM gateway AS gateway_image
ENTRYPOINT ["python", "-m", "api_gateway.app"]