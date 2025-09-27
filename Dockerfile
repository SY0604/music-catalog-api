# Base Python runtime environment
FROM python:3.11-slim

# Configure environment variables for optimal Python execution
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set application working directory
WORKDIR /application

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade package manager and install core dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi[standard]
RUN pip install --no-cache-dir pymongo
RUN pip install --no-cache-dir beanie[odm]
RUN pip install --no-cache-dir motor
RUN pip install --no-cache-dir aiohttp

# Copy application source code
COPY . .

# Expose application port
EXPOSE 8000

# Start the application server
CMD ["uvicorn", "src.server:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
