FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create required directories
RUN mkdir -p models config shared

# Copy configuration files if they exist
COPY config/ ./config/
COPY shared/ ./shared/

# Copy main application file
COPY main.py ./

# Create empty model file if it doesn't exist
RUN touch models/emotion_model.pt

# Expose the port (optional, Render auto-detects)
EXPOSE 8000

# Start with the port assigned by Render.com
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4"]
