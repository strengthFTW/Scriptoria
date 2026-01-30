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
    
    # Type Guard: Ensure screenplay_data and characters are valid
    if not isinstance(screenplay_data, dict):
        raise ValueError("Scene generator received invalid screenplay data. Please try regenerating.")
    if not isinstance(characters, list):
        raise ValueError("Scene generator received invalid character data. Please try regenerating.")
    
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
        response = client.generate(prompt, json_mode=True)
        result = safe_parse_json(response)
        
        if isinstance(result, dict):
            # If AI returned a dict, try to find the list inside
            print("⚠️ AI returned dict, attempting to extract list...")
            for key in ['scenes', 'breakdown', 'data', 'result']:
                if key in result and isinstance(result[key], list):
                    result = result[key]
                    break
            else:
                # If no specific key found, take the first list value found
                for value in result.values():
                    if isinstance(value, list):
                        result = value
                        break
        
        if not isinstance(result, list):
            raise ValueError(f"AI returned {type(result).__name__} instead of a list for scenes.")
            
        return result
        
    except Exception as e:
        print(f"❌ Scene generation error: {e}")
        if 'response' in locals() and response:
            print(f"Full response for debugging: {response}")
        raise Exception(f"Failed to generate scenes: {str(e)}")
