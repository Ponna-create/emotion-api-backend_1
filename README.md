# Emotion Detection API

A multilingual emotion detection API with support for 10 emotions and emoji analysis. The project includes both local development and production-ready environments.

## Features

- Multilingual emotion detection (10 emotions)
- Emoji extraction and analysis
- Language detection
- Confidence scores and probability distribution
- Production features:
  - Rate limiting (10 requests/minute)
  - API key authentication
  - Auto-scaling configuration
  - Health monitoring
  - Usage metrics

## Project Structure

```
final_api/
├── local/                  # Local development version
│   ├── main.py            # FastAPI app (no auth/rate limit)
│   ├── test_request.py    # Test script
│   └── requirements.txt   # Dependencies
├── production/            # Production version
│   ├── main.py           # FastAPI app with auth/rate limit
│   ├── Dockerfile        # Container configuration
│   ├── render.yaml       # Render.com deployment config
│   ├── test_request.py   # Test script with auth
│   └── requirements.txt  # Dependencies with extra packages
├── shared/               # Shared components
│   ├── model_utils.py    # Model loading and prediction
│   ├── emotion_labels.py # Emotion definitions
│   └── helpers.py        # Utility functions
└── README.md             # This file
```

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   cd local
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Test the API:
   ```bash
   python test_request.py
   ```

The local API will be available at `http://localhost:8000`.

## Production Deployment

### Running Locally with Docker

1. Build the container:
   ```bash
   cd production
   docker build -t emotion-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 emotion-api
   ```

3. Test with authentication:
   ```bash
   python test_request.py --api-key your_api_key
   ```

### Deploying to Render.com

1. Push your code to GitHub

2. Create a new Web Service on Render.com:
   - Connect your repository
   - Select "Docker" as environment
   - Use the `production/render.yaml` configuration

3. Set up environment variables:
   - Add your API keys through the Render dashboard
   - Configure any other necessary secrets

## API Documentation

### Endpoints

- `GET /` - API information
- `GET /emotions` - List supported emotions
- `POST /analyze` - Analyze text (requires API key in production)
- `GET /metrics/usage` - Get API usage (requires API key)
- `GET /health` - Health check

### Example Request (Production)

```python
import requests

headers = {"x-api-key": "your_api_key"}
data = {"text": "I'm so happy today! 😊"}

response = requests.post(
    "http://localhost:8000/analyze",
    json=data,
    headers=headers
)
print(response.json())
```

### Response Format

```json
{
  "text": "I'm so happy today! 😊",
  "predicted_emotion": "joy",
  "confidence": 0.95,
  "language": "en",
  "emojis": ["😊"],
  "emotion_probabilities": [
    {"emotion": "joy", "probability": 0.95},
    {"emotion": "love", "probability": 0.03},
    ...
  ]
}
```

## Rate Limiting

The production API implements rate limiting:
- Basic tier: 10 requests/minute
- Pro tier: 100 requests/minute

## Error Handling

- 400: Invalid input
- 401: Missing/invalid API key
- 429: Rate limit exceeded
- 500: Server error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 