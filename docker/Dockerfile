FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-dev.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements-dev.txt

# Copy project requirements
COPY languages/python/projects/interview-patterns-api/requirements.txt \
     /tmp/interview-patterns-requirements.txt
COPY languages/python/projects/interview-prep-capstone/requirements.txt \
     /tmp/interview-prep-requirements.txt

RUN pip install -r /tmp/interview-patterns-requirements.txt && \
    pip install -r /tmp/interview-prep-requirements.txt && \
    rm /tmp/*-requirements.txt

# Set default shell
SHELL ["/bin/bash", "-c"]

# Default command
CMD ["/bin/bash"]
