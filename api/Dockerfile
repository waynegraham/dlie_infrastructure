# api/Dockerfile

# 1. Use a slim Python image
FROM python:3.10-slim

# 2. Set a working directory at /app
WORKDIR /app

# 3. Copy only requirements first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your API code into /app/api
COPY . ./api

# 6. Tell Python to look in /app for imports
ENV PYTHONPATH=/app

# 7. Expose the port Uvicorn will serve on
EXPOSE 8000

# 8. Run the FastAPI app via the api package
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]