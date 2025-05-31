FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt from production/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy model files and tokenizer from shared/models/phase3 to /app/model
COPY ../shared/models/phase3 /app/model

# Copy main.py from production/
COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
