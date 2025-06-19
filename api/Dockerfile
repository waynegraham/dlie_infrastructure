# api/Dockerfile
# Multi-stage build for Python FastAPI application

### Builder stage: install dependencies
FROM python:3.10-slim AS builder
WORKDIR /build

# Install Python dependencies to a local directory
COPY api/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

### Final stage: application image
FROM python:3.10-slim AS runtime

# Create a non-root user for running the app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY api ./api

# Unbuffered stdout/stderr (for logging)
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Default command: run the FastAPI app via Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]