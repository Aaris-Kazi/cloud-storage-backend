# Use an official Python image as base
FROM python:3.10

# Set environment variables to prevent Python from buffering outputs
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files (if using Django static files)
RUN python manage.py collectstatic --noinput

# Expose port (WSO2 Choreo uses dynamic port allocation)
EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "cloud_drive.wsgi:application", "--bind", "0.0.0.0:8000"]
