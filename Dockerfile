# Use official Python image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install required for mysqlclient and gunicorn
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the rest of your app code
COPY . .

# Expose Flask/Gunicorn port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py

# Start using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
