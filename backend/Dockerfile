FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies and supervisor
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create directory for SQLite database and set permissions
RUN mkdir -p /app/backend && \
    chown -R 1000:1000 /app/backend && \
    chmod 777 /app/backend

# Copy requirements and install dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the adalace package and install it
COPY adalace-engine/ /app/adalace-engine/
RUN pip install -e /app/adalace-engine/

# Enable Python optimizations
ENV PYTHONOPTIMIZE=1
ENV PYTHONUNBUFFERED=1

# Copy application code
COPY backend/ /app/backend/

# Setup supervisor configuration
COPY backend/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]