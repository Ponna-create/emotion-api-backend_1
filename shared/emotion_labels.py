# -*- coding: utf-8 -*-
"""
Emotion labels and descriptions for the multilingual emotion classifier.
"""

EMOTION_LABELS = [
    'anger',
    'fear',
    'hate',
    'joy',
    'love',
    'lust',
    'neutral',
    'positive',
    'sadness',
    'sarcasm'
]

EMOTION_DESCRIPTIONS = {
    'anger': 'Strong feeling of annoyance, displeasure, or hostility',
    'fear': 'Emotion caused by threat or danger',
    'hate': 'Intense dislike or aversion',
    'joy': 'Feeling of great pleasure and happiness',
    'love': 'Deep affection or romantic attachment',
    'lust': 'Strong sexual desire or appetite',
    'neutral': 'No strong emotional content',
    'positive': 'General positive sentiment or approval',
    'sadness': 'Feeling of sorrow or unhappiness',
    'sarcasm': 'Use of irony to mock or convey contempt'
}

# Examples for API documentation
EXAMPLE_TEXTS = {
    'anger': 'I can\'t believe they cancelled my favorite show! 😠',
    'fear': 'I\'m really scared about tomorrow\'s presentation 😨',
    'hate': 'I absolutely despise this kind of behavior 😡',
    'joy': 'Just got promoted at work! So happy! 🎉',
    'love': 'You mean the world to me ❤️',
    'lust': 'You look absolutely stunning tonight 🔥',
    'neutral': 'The meeting is scheduled for 3pm.',
    'positive': 'Great work on the project! 👍',
    'sadness': 'Missing you so much... 😢',
    'sarcasm': 'Oh great, another Monday... 🙄'
} 