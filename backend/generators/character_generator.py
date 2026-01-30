"""
Character Generator using Gemini API
Generates character profiles based on screenplay
"""
import json
import re
from utils.ai_client import get_ai_client

def generate_characters(screenplay_data: dict) -> list:
    """
    Generate character profiles from screenplay outline
    
    Args:
        screenplay_data: Screenplay outline dictionary
        
    Returns:
        List of character dictionaries
    """
    client = get_ai_client()
    
    title = screenplay_data.get('title', 'Untitled')
    logline = screenplay_data.get('logline', '')
    genre = screenplay_data.get('genre', 'Drama')
    
    prompt = f"""You are a character development expert. Based on this screenplay outline, create 3-5 compelling character profiles.

Title: {title}
Logline: {logline}
Genre: {genre}

Generate character profiles in this JSON format:

[
    {{
        "name": "Character name",
        "role": "Protagonist/Antagonist/Supporting",
        "arc": "Brief description of their character arc",
        "traits": ["Trait 1", "Trait 2", "Trait 3"]
    }}
]

Create diverse, three-dimensional characters that fit the story. Return ONLY the JSON array, no additional text."""

    try:
        response = client.generate(prompt)
        
        # Extract JSON from response
        json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            json_str = json_match.group(0) if json_match else response
        
        characters = json.loads(json_str)
        return characters
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        raise Exception("Failed to parse AI response as JSON")
    except Exception as e:
        print(f"❌ Generation error: {e}")
        raise
