FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt from production/
COPY production/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy shared directory from repo root
COPY shared /app/shared

# (Optional) Copy models and tokenizer if needed
COPY models /app/models
COPY tokenizer /app/tokenizer

# Copy main.py from production/
COPY production/main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
