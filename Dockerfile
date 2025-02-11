# Use an official Python image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies in a single RUN command (reduces image layers)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    gcc \
    pkg-config \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/storage && -R 777 /app/storage  
# Copy application files
COPY . .

# Copy sensitive files
COPY /run/etc.xml /app/run/etc.xml
COPY /run/ca.pem /app/run/ca.pem

# Create a non-root user (Fix for CKV_CHOREO_1)
RUN groupadd --gid 10001 appgroup && \
    useradd --uid 10001 --gid 10001 --create-home appuser && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER 10001

# Expose port
EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cloud_drive.wsgi"]
