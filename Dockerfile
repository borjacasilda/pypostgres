# Use official Python runtime as base image
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /build

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# Development/Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser

# Set work directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy project files
COPY --chown=appuser:appuser . .

# Create logs directory with proper permissions
RUN mkdir -p logs && chown -R appuser:appuser logs

# Switch to non-root user
USER appuser

# Expose port (for future API extensions)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.postgres_manager import PostgresManager; PostgresManager().connect(); print('OK')" || exit 1

# Default command
CMD ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]

# Labels for metadata
LABEL maintainer="Your Name <your-email@example.com>" \
      version="1.0.0" \
      description="PyPostgres - Professional PostgreSQL wrapper for Python"
