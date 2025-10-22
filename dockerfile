# Dockerfile for NZQA Certificate Generator Demo
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* 

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY images/ ./images/
COPY fonts/ ./fonts/
COPY app.py .
COPY .streamlit/config.toml .streamlit/

# Expose Streamlit port
EXPOSE 7500

# Health check
HEALTHCHECK CMD curl --fail http://localhost:7500/_stcore/health

# Run Streamlit with explicit configuration
CMD ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false"]