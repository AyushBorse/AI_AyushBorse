FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories for output and storage
RUN mkdir -p output storage

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "cognimate.api.app:app", "--host", "0.0.0.0", "--port", "8000"]