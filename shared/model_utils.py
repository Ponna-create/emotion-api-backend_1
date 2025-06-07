"""
Model utilities for emotion detection.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
from typing import Dict, Optional
import logging
from pathlib import Path

from .helpers import (
    extract_emojis,
    detect_language,
    normalize_text,
    format_probabilities
)
from .emotion_labels import EMOTION_LABELS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionDetector:
    def __init__(
        self,
        model_path: str,
        config_path: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        Initialize emotion detector.
        
        Args:
            model_path: Path to saved model weights
            config_path: Optional path to model config
            device: Optional device to run model on
        """
        # Set device
        self.device = (
            device if device
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )
        logger.info(f"Using device: {self.device}")
        
        # Load config if provided
        self.config = {}
        if config_path:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        
        # Set model name from config or use default
        model_name = (
            self.config.get('model', {}).get('name')
            or "distilbert-base-multilingual-cased"
        )
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(EMOTION_LABELS)
        ).to(self.device)
        
        # Load trained weights
        try:
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            logger.info("Model weights loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model weights: {str(e)}")
            raise
            
        self.model.eval()
    
    def predict(self, text: str) -> Dict:
        """
        Predict emotion for input text.
        
        Returns dict with:
        - predicted emotion
        - confidence score
        - detected language
        - extracted emojis
        - emotion probabilities
        """
        # Extract metadata
        lang = detect_language(text)
        emojis = extract_emojis(text)
        
        # Preprocess text
        processed_text = normalize_text(text)
        
        # Tokenize
        max_length = self.config.get('model', {}).get('max_length', 128)
        inputs = self.tokenizer(
            processed_text,
            max_length=max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
            pred_idx = torch.argmax(probs).item()
            confidence = probs[pred_idx].item()
        
        # Get emotion probabilities
        emotion_probs = {
            emotion: probs[idx].item()
            for idx, emotion in enumerate(EMOTION_LABELS)
        }
        
        return {
            "text": text,
            "predicted_emotion": EMOTION_LABELS[pred_idx],
            "confidence": confidence,
            "language": lang,
            "emojis": emojis,
            "emotion_probabilities": format_probabilities(emotion_probs)
        }

def load_model(
    model_path: str,
    config_path: Optional[str] = None,
    device: Optional[str] = None
) -> EmotionDetector:
    """Load and initialize the emotion detection model."""
    try:
        detector = EmotionDetector(
            model_path=model_path,
            config_path=config_path,
            device=device
        )
        return detector
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise 