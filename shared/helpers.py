"""
Helper functions for text processing and analysis.
"""

import emoji
from langdetect import detect
from typing import List, Dict, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_emojis(text: str) -> List[str]:
    """Extract emojis from text."""
    return [c for c in text if c in emoji.EMOJI_DATA]

def detect_language(text: str) -> str:
    """
    Detect language of input text.
    Returns 'unknown' if detection fails.
    """
    try:
        return detect(text)
    except:
        return "unknown"

def normalize_text(text: str) -> str:
    """
    Normalize text by:
    - Adding spaces around emojis
    - Converting to lowercase
    - Removing extra whitespace
    """
    # Add spaces around emojis
    text = emoji.replace_emoji(text, lambda chars, *args: f" {chars} ")
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    return text

def format_probabilities(probs: Dict[str, float]) -> List[Dict[str, float]]:
    """
    Format probability dictionary into sorted list for API response.
    """
    return [
        {"emotion": emotion, "probability": prob}
        for emotion, prob in sorted(
            probs.items(),
            key=lambda x: x[1],
            reverse=True
        )
    ]

def validate_input(text: str) -> Tuple[bool, str]:
    """
    Validate input text.
    Returns (is_valid, error_message).
    """
    if not text:
        return False, "Text cannot be empty"
    if len(text.strip()) == 0:
        return False, "Text cannot be only whitespace"
    if len(text) > 1000:
        return False, "Text must be less than 1000 characters"
    return True, "" 