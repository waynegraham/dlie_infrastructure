# syntax=docker/dockerfile:1.4

# ---------------------------------------
# 1) Builder stage: install deps & cache
# ---------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install OS-level dependencies and Git LFS (optional)
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker layer caching
COPY api/requirements.txt ./api/requirements.txt

# Install Python dependencies with pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r ./api/requirements.txt

# ---------------------------------------
# 2) Runtime stage: assemble image
# ---------------------------------------
FROM python:3.12-slim

WORKDIR /app

# Create non-root user and cache directory
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1001 appuser && \
    mkdir -p /cache && chown -R appuser:appgroup /cache

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . /app

# Environment for Transformer cache
ENV HF_HOME=/cache\
    TRANSFORMERS_CACHE=/cache

# Expose port and switch user
EXPOSE 8000
USER appuser

# Launch FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]