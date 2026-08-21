FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MCP server source
COPY server.py .

# Expose the MCP port
EXPOSE 8765

# Start the server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8765", "--workers", "2"]
