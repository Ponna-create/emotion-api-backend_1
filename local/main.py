"""
Local development version of the Emotion Detection API.
No authentication or rate limiting.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from pathlib import Path
import sys

# Add parent directory to path to import shared modules
sys.path.append(str(Path(__file__).parent.parent))

from shared.model_utils import load_model
from shared.helpers import validate_input
from shared.emotion_labels import EMOTION_LABELS, EMOTION_DESCRIPTIONS, EXAMPLE_TEXTS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Emotion Detection API (Local)",
    description="Local development version of the Emotion Detection API",
    version="1.0.0"
)

# Model paths
MODEL_PATH = os.path.join("..", "models", "phase3", "best_model.pt")
CONFIG_PATH = os.path.join("..", "config", "training_config.json")

# Input model
class TextInput(BaseModel):
    text: str
    
    class Config:
        schema_extra = {
            "example": {
                "text": EXAMPLE_TEXTS['joy']
            }
        }

# Load model
try:
    detector = load_model(MODEL_PATH, CONFIG_PATH)
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "name": "Emotion Detection API (Local)",
        "version": "1.0.0",
        "description": "Local development version for testing",
        "endpoints": {
            "/": "This information",
            "/analyze": "POST endpoint for emotion analysis",
            "/emotions": "GET list of supported emotions",
            "/health": "GET health check"
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
def analyze_text(input_data: TextInput):
    """
    Analyze text for emotion detection.
    
    Returns:
    - predicted emotion
    - confidence score
    - detected language
    - extracted emojis
    - emotion probabilities
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

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": "loaded" if detector else "not_loaded"
    } 