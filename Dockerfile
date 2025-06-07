FROM python:3.10-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create required folders and copy configs
RUN mkdir -p models config shared
COPY config/ ./config/
COPY shared/ ./shared/
COPY main.py .

# Ensure models directory exists and has correct permissions
RUN mkdir -p shared/models/phase3
RUN chmod -R 755 shared/models

# Railway default port is 5000 (set $PORT fallback)
ENV PORT=5000
EXPOSE 5000

# Launch FastAPI with Uvicorn using dynamic port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
