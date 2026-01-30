"""
AI Client for Groq API integration
100% FREE - No credit card required!
Super fast: 70+ tokens/second
"""
import os
from groq import Groq
import httpx
from typing import Optional

class AIClient:
    def __init__(self):
        """Initialize Groq API client (100% FREE!)"""
        self.api_key = os.getenv('GROQ_API_KEY', '')
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Create httpx client with proxy detection disabled
        http_client = httpx.Client(trust_env=False)
        
        # Groq client - OpenAI compatible
        self.client = Groq(api_key=self.api_key, http_client=http_client)
        self.model = "llama-3.3-70b-versatile"  # Fast and creative
    
    def generate(self, prompt: str, max_retries: int = 2) -> Optional[str]:
        """
        Generate content using Groq API
        
        Args:
            prompt: The prompt to send to the AI
            max_retries: Number of retries on failure
            
        Returns:
            Generated text or None on failure
        """
        for attempt in range(max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a professional screenplay writer and story consultant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=2048
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries:
                    raise Exception(f"Failed to generate content after {max_retries + 1} attempts: {str(e)}")
        
        return None

# Global client instance
_client = None

def get_ai_client() -> AIClient:
    """Get or create the global AI client instance"""
    global _client
    if _client is None:
        _client = AIClient()
    return _client
