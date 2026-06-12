# =============================================================================
# FRIDAY AI — Headless Docker Image
# Use this for server deployments (no GUI, no voice, no HUD).
# =============================================================================
FROM python:3.11-slim

LABEL maintainer="FRIDAY AI" \
      description="Headless FRIDAY AI assistant for server deployments"

# Install system dependencies for browser engine, media processing, and PDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    pandoc \
    wkhtmltopdf \
    portaudio19-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY requirements_full.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements_full.txt \
    && pip install --no-cache-dir playwright \
    && playwright install chromium \
    && playwright install-deps chromium

# Copy source code
COPY . .

# Override config for headless mode (disable GUI features)
COPY config_production.json .

# Create output directories
RUN mkdir -p output generated memory_db logs

# Expose ports for optional web interface or API
EXPOSE 8000

# Default command — override with CMD if you want specific behavior
CMD ["python", "run_friday.py"]
