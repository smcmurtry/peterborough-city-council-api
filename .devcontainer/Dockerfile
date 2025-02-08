FROM python:3.11-slim

# Install basic development tools
RUN apt-get update && apt-get install -y \
    git \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional development dependencies
RUN pip install --no-cache-dir \
    black \
    flake8 \
    pytest
