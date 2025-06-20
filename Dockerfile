# Use slim Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set work directory
WORKDIR /app

# Install system dependencies for mysqlclient and security
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libffi-dev \
    libssl-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user and switch to it
RUN useradd -m nonrootuser
USER nonrootuser

# Expose port (must match Gunicorn binding)
EXPOSE 5000

# Run Gunicorn as production WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
