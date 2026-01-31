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
        
        # Robust list extraction if AI returns an object instead of a direct array
        if isinstance(result, dict):
            print(f"⚠️ AI returned dict with keys: {list(result.keys())}, attempting to extract list...")
            
            # 1. Broad list of common keys AI might use for scenes
            common_keys = [
                'scenes', 'breakdown', 'scene_breakdown', 'sceneBreakdown',
                'scene_list', 'sceneList', 'data', 'result', 'list', 'items'
            ]
            
            for key in common_keys:
                if key in result and isinstance(result[key], list):
                    print(f"✅ Found scene list under key: '{key}'")
                    result = result[key]
                    break
            else:
                # 2. If no common key found, search for ONLY list found in top-level values
                lists_found = [v for v in result.values() if isinstance(v, list)]
                if len(lists_found) == 1:
                    print("✅ Found exactly one list in response, assuming it's the scene list")
                    result = lists_found[0]
                elif len(lists_found) > 1:
                    # Pick the largest list if multiple lists found
                    print(f"✅ Found {len(lists_found)} lists, picking the largest one")
                    result = max(lists_found, key=len)
        
        if not isinstance(result, list):
            raise ValueError(f"AI returned {type(result).__name__} instead of a list. Keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
            
        return result
        
    except Exception as e:
        print(f"❌ Scene generation error: {e}")
        if 'response' in locals() and response:
            print(f"Full response for debugging: {response}")
        raise Exception(f"Failed to generate scenes: {str(e)}")
