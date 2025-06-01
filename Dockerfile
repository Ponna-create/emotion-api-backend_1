FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary application files and folders
COPY main.py ./
COPY shared/ ./shared/
COPY models/ ./models/
COPY config/ ./config/

# Create required directories if they don't exist
RUN mkdir -p models config

# Expose the port (optional, Render auto-detects)
EXPOSE 8000

# Start with the port assigned by Render.com
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4"]
