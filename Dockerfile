# NSS X - National Spatial Strategy for Saudi Arabia
# Docker Container for Streamlit Dashboard

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Install system dependencies for geospatial libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libspatialindex-dev \
    gdal-bin \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Create app directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements-docker.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-docker.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/
COPY 01_data/ ./01_data/
COPY .streamlit/ ./.streamlit/

# Create necessary directories
RUN mkdir -p 02_analytics 03_scenarios 04_strategy 05_governance 06_deliverables

# Expose Streamlit port
EXPOSE 8501

# Copy analytics outputs
COPY 02_analytics/ ./02_analytics/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Complete Dashboard (all workstreams)
CMD ["streamlit", "run", "scripts/dashboard_complete.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
