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
    def generate(self, prompt: str, max_retries: int = 2, json_mode: bool = False) -> Optional[str]:
        """
        Generate content with automatic model fallback for rate limits.
        """
        # List of models to try in order of preference
        models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "llama-3.1-8b-instant"
        ]
        
        last_error = None
        
        for model in models:
            for attempt in range(max_retries + 1):
                try:
                    system_content = "You are a professional screenplay writer and story consultant."
                    if json_mode:
                        system_content += " You MUST respond with a valid JSON object ONLY. No other text."

                    params = {
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.8 if json_mode else 0.9,
                        "max_tokens": 4096 if json_mode else 2048,
                    }

                    if json_mode:
                        params["response_format"] = {"type": "json_object"}

                    response = self.client.chat.completions.create(**params)
                    return response.choices[0].message.content
                
                except Exception as e:
                    last_error = e
                    error_msg = str(e).lower()
                    
                    # If it's a rate limit (429), try the next model immediately
                    if "rate_limit_exceeded" in error_msg or "429" in error_msg:
                        print(f"⚠️  Rate limit on {model}, trying next available model...")
                        break # Break inner loop to try next model
                    
                    print(f"⚠️  Attempt {attempt + 1} with {model} failed: {str(e)}")
                    if attempt == max_retries:
                        print(f"❌ All retries for {model} failed.")
        
        raise Exception(f"AI Generation failed across all fallback models. Last error: {str(last_error)}")

# Global client instance
_client = None

def get_ai_client() -> AIClient:
    """Get or create the global AI client instance"""
    global _client
    if _client is None:
        _client = AIClient()
    return _client
