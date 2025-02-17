FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the updated code including the entrypoint script
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/backend/entrypoint.sh

# Set the entrypoint to your script
ENTRYPOINT ["/app/backend/entrypoint.sh"]
