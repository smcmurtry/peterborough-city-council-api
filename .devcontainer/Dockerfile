FROM python:3.11-slim

# Install basic development tools and zsh
RUN apt-get update && apt-get install -y \
    git \
    make \
    curl \
    zsh \
    && rm -rf /var/lib/apt/lists/*

# Install Oh My Zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Set zsh as default shell
ENV SHELL /bin/zsh

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
