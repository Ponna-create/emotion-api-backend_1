"""
Test script for the production Emotion Detection API.
Tests authentication and rate limiting.
"""

import requests
import json
import time
from typing import Dict, Optional

def test_api(api_key: str = "test_key", base_url: str = "http://localhost:8000"):
    """
    Test the production API endpoints.
    
    Args:
        api_key: API key to use for authentication
        base_url: Base URL of the API
    """
    # Headers for authenticated requests
    headers = {"x-api-key": api_key}
    
    def make_request(
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        expected_status: int = 200
    ):
        """Make a request and check the response."""
        url = f"{base_url}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, json=data, headers=headers)
            
        print(f"\n{method} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print("Error:", response.text)
            
        return response
    
    # Test cases
    print("\nTesting Emotion Detection API (Production)")
    print("-" * 50)
    
    # Test root endpoint (no auth required)
    make_request("GET", "/")
    
    # Test emotions endpoint (no auth required)
    make_request("GET", "/emotions")
    
    # Test health endpoint (no auth required)
    make_request("GET", "/health")
    
    # Test invalid API key
    print("\nTesting invalid API key")
    headers["x-api-key"] = "invalid_key"
    make_request("POST", "/analyze", {"text": "Test"}, 401)
    headers["x-api-key"] = api_key
    
    # Test rate limiting
    print("\nTesting rate limiting (10 requests/minute)")
    test_text = "I'm so happy today! 😊"
    
    for i in range(12):
        print(f"\nRequest {i+1}")
        response = make_request(
            "POST",
            "/analyze",
            {"text": test_text},
            200 if i < 10 else 429
        )
        if i < 11:  # Don't sleep after last request
            time.sleep(1)  # Sleep to make output readable
            
    # Test usage metrics
    make_request("GET", "/metrics/usage")
    
    # Test various text inputs
    print("\nTesting different text inputs")
    test_cases = [
        "This is amazing! 🎉",  # Joy with emoji
        "I hate this so much 😠",  # Anger with emoji
        "क्या बात है! 👏",  # Hindi with emoji
        "எனக்கு ரொம்ப பிடிக்கும் ❤️",  # Tamil with emoji
        "This makes me 😊 and 😢",  # Mixed emotions
        "This is a very long text " * 100  # Too long
    ]
    
    for text in test_cases:
        make_request("POST", "/analyze", {"text": text})
        time.sleep(6)  # Sleep to avoid rate limit

if __name__ == "__main__":
    test_api() 