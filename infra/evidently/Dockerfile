# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Evidently
RUN pip install --no-cache-dir evidently==0.7.7

# Create workspace directory
RUN mkdir -p /app/workspace

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command to run Evidently UI server
CMD ["evidently", "ui", "--workspace", "/app/workspace", "--host", "0.0.0.0", "--port", "8000"]