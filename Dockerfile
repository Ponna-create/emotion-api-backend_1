FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY production/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code and main app code
COPY shared /app/shared
COPY production/main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
