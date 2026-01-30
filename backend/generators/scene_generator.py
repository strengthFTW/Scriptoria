"""
Scene Generator using Groq API
Generates scene breakdown based on screenplay and characters
"""
import json
import re
from utils.ai_client import get_ai_client
from utils.json_helper import safe_parse_json

def generate_scenes(screenplay_data: dict, characters: list) -> list:
    """
    Generate scene breakdown from screenplay and characters
    
    Args:
        screenplay_data: Screenplay outline dictionary
        characters: List of character dictionaries
        
    Returns:
        List of scene dictionaries
    """
    client = get_ai_client()
    
    title = screenplay_data.get('title', 'Untitled')
    logline = screenplay_data.get('logline', '')
    genre = screenplay_data.get('genre', 'Drama')
    
    # Extract character names for context
    character_names = [char.get('name', 'Unknown') for char in characters]
    
    prompt = f"""You are a film production expert. Based on this screenplay outline, create a detailed scene breakdown.

Title: {title}
Logline: {logline}
Genre: {genre}
Characters: {', '.join(character_names)}

CRITICAL: When listing characters in scenes, you MUST use the EXACT names from the Characters list above: {', '.join(character_names)}
Do NOT use different names or variations. Only use the names provided.

Generate 8-12 scenes in this JSON format:

[
    {{
        "sceneNumber": 1,
        "location": "Location name (INT/EXT)",
        "timeOfDay": "DAY/NIGHT/MORNING/EVENING",
        "characters": ["EXACT name from Characters list", "EXACT name from Characters list"],
        "action": "Brief description of what happens in this scene",
        "duration": "Estimated minutes"
    }}
]

Create a complete scene breakdown that covers the full story arc. Return ONLY the JSON array, no additional text."""


    try:
        response = client.generate(prompt)
        return safe_parse_json(response)
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response: {response[:500]}...")
        raise Exception("Failed to parse AI response as JSON")
    except Exception as e:
        print(f"❌ Generation error: {e}")
        raise
