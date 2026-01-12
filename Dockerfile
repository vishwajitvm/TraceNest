# Use official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure stdout/stderr are unbuffered
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install package in editable mode (for development verification)
RUN pip install --no-cache-dir .

# Default command: run basic example
CMD ["python", "examples/basic.py"]
