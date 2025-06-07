# -*- coding: utf-8 -*-
"""
Emotion labels and descriptions for the multilingual emotion classifier.
"""

EMOTION_LABELS = [
    'positive',
    'negative',
    'neutral',
    'sarcasm',
    'questions'
]

EMOTION_DESCRIPTIONS = {
    'positive': 'General positive sentiment or approval',
    'negative': 'General negative sentiment or disapproval',
    'neutral': 'No strong emotional content',
    'sarcasm': 'Use of irony to mock or convey contempt',
    'questions': 'Expressions of inquiry or curiosity'
}

# Examples for API documentation
EXAMPLE_TEXTS = {
    'positive': 'Great work on the project! 👍',
    'negative': 'This is the worst update ever. 👎',
    'neutral': 'The meeting is scheduled for 3pm.',
    'sarcasm': 'Oh great, another Monday... 🙄',
    'questions': 'When is the next video coming out? 🤔'
} 