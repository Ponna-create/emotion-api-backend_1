"""
Production version of the Emotion Detection API.
Includes rate limiting and API key authentication.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import os
from pathlib import Path
import sys
from typing import Dict, List
import json
import torch

# Add shared modules path
sys.path.append(str(Path(__file__).parent))

from shared.model_utils import load_model
from shared.helpers import validate_input
from shared.emotion_labels import EMOTION_LABELS, EMOTION_DESCRIPTIONS, EXAMPLE_TEXTS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Emotion Detection API",
    description="Production version with rate limiting and authentication",
    version="1.0.0"
)

# Add rate limit error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model and config paths
MODEL_PATH = os.path.join("shared", "models", "phase3", "best_model.pt")
CONFIG_PATH = os.path.join("config", "training_config.json")

# API key configuration
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Load API keys from config
try:
    with open(os.path.join("config", "api_keys.json")) as f:
        API_KEYS = json.load(f)
except FileNotFoundError:
    logger.warning("API keys file not found, using default test key")
    API_KEYS = {
        "test_key": {"tier": "basic", "rate_limit": "10/minute"}
    }

# Input model
class TextInput(BaseModel):
    text: str
    
    class Config:
        schema_extra = {
            "example": {
                "text": EXAMPLE_TEXTS['positive']
            }
        }

# Load model
try:
    detector = load_model(MODEL_PATH, CONFIG_PATH)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

async def get_api_key(
    api_key_header: str = Depends(api_key_header)
) -> Dict:
    """Validate API key and return key info."""
    if not api_key_header:
        raise HTTPException(
            status_code=401,
            detail="API key is required"
        )
    
    key_info = API_KEYS.get(api_key_header)
    if not key_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return key_info

@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "name": "Emotion Detection API",
        "version": "1.0.0",
        "description": "Production API with rate limiting and authentication",
        "endpoints": {
            "/": "This information",
            "/analyze": "POST endpoint for emotion analysis (requires API key)",
            "/emotions": "GET list of supported emotions",
            "/metrics/usage": "GET API usage metrics (requires API key)",
            "/health": "GET health check"
        },
        "authentication": {
            "header": API_KEY_NAME,
            "tiers": {
                "basic": "10 requests/minute",
                "pro": "100 requests/minute"
            }
        }
    }

@app.get("/emotions")
def get_emotions():
    """Get list of supported emotions and descriptions."""
    return {
        "emotions": [
            {
                "name": emotion,
                "description": EMOTION_DESCRIPTIONS[emotion],
                "example": EXAMPLE_TEXTS[emotion]
            }
            for emotion in EMOTION_LABELS
        ]
    }

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze_text(
    request: Request,
    input_data: TextInput,
    key_info: Dict = Depends(get_api_key)
):
    """
    Analyze text for emotion detection.
    Requires API key and respects rate limits.
    """
    # Validate input
    is_valid, error_msg = validate_input(input_data.text)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    try:
        # Get prediction
        result = detector.predict(input_data.text)
        return result
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during analysis"
        )

@app.get("/metrics/usage")
async def get_usage_metrics(
    key_info: Dict = Depends(get_api_key)
):
    """Get API usage metrics for the authenticated key."""
    return {
        "tier": key_info["tier"],
        "rate_limit": key_info["rate_limit"],
        "requests_remaining": "Not implemented"
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": "loaded" if detector else "not_loaded"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) 