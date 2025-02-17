# Use lightweight Python image
FROM python:3.10-slim

# Install dependencies (keep minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app/backend

# Copy dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/backend/entrypoint.sh

# Set the entrypoint to your script
ENTRYPOINT ["/app/backend/entrypoint.sh"]
