FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and all necessary folders/files
COPY main.py .
COPY shared ./shared
COPY models ./models
COPY config ./config

# Expose the port (optional, Render auto-detects)
EXPOSE 8000

# Start with the port assigned by Render.com
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4"]
