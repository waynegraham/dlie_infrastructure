# Start with your base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Ensure apt lists are updated and install 'passwd' package for robust user management.
# Then, create the non-root user and group.
RUN apt-get update && \
    apt-get install -y --no-install-recommends passwd && \
    groupadd -r appgroup && \
    useradd -r -g appgroup -u 1001 appuser && \
    rm -rf /var/lib/apt/lists/*

# Copy your requirements files and install dependencies
COPY api/requirements.txt ./api/requirements.txt
RUN pip install --no-cache-dir -r ./api/requirements.txt

# Create the /cache directory and set its ownership to 'appuser' during the build.
# This ensures that when the 'transformer_cache' volume is first initialized
# at /cache, it inherits these permissions.
RUN mkdir -p /cache && chown -R appuser:appgroup /cache

# Copy the rest of your application code
COPY . /app

# Set environment variables
ENV HF_HOME=/cache

# Expose the port
EXPOSE 8000

# Switch to the non-root user for running the application
USER appuser

# Define the command to run your FastAPI application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]