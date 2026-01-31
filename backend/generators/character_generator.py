"""
Character Generator using Gemini API
Generates character profiles based on screenplay
"""
import json
import re
from utils.ai_client import get_ai_client
from utils.json_helper import safe_parse_json

def generate_characters(screenplay_data: dict) -> list:
    """
    Generate character profiles from screenplay outline
    
    Args:
        screenplay_data: Screenplay outline dictionary
        
    Returns:
        List of character dictionaries
    """
    client = get_ai_client()
    
    # Safety check: if screenplay_data is a string, we can't parse it
    if isinstance(screenplay_data, str):
        raise ValueError("Character generator received a string instead of screenplay data. Please try regenerating.")
    
    title = screenplay_data.get('title', 'Untitled')
    logline = screenplay_data.get('logline', '')
    genre = screenplay_data.get('genre', 'Drama')
    main_characters = screenplay_data.get('mainCharacters', [])
    
    # Extract character names from the screenplay
    character_names_str = ", ".join(main_characters) if main_characters else "the main characters"
    
    prompt = f"""You are a character development expert. Based on this screenplay outline, create detailed character profiles.

Title: {title}
Logline: {logline}
Genre: {genre}
Main Characters: {character_names_str}

CRITICAL: You MUST use the EXACT character names listed above: {character_names_str}
Do NOT create new character names. Only develop profiles for the characters already named in the outline.

Generate character profiles in this JSON format:

[
    {{
        "name": "EXACT name from the Main Characters list above",
        "role": "Protagonist/Antagonist/Supporting",
        "arc": "Brief description of their character arc",
        "traits": ["Trait 1", "Trait 2", "Trait 3"]
    }}
]

Create 3-5 diverse, three-dimensional characters that fit the story. Return ONLY the JSON array, no additional text."""

    try:
        response = client.generate(prompt, json_mode=True)
        result = safe_parse_json(response)
        
        # Robust list extraction if AI returns an object instead of a direct array
        if isinstance(result, dict):
            print(f"⚠️ AI returned dict with keys: {list(result.keys())}, attempting to extract list...")
            
            # 1. Broad list of common keys AI might use for characters
            common_keys = [
                'characters', 'profiles', 'character_profiles', 'characterProfiles',
                'character_data', 'characterData', 'main_characters', 'mainCharacters',
                'data', 'result', 'list', 'items'
            ]
            
            for key in common_keys:
                if key in result and isinstance(result[key], list):
                    print(f"✅ Found character list under key: '{key}'")
                    result = result[key]
                    break
            else:
                # 2. If no common key found, search for ONLY list found in top-level values
                lists_found = [v for v in result.values() if isinstance(v, list)]
                if len(lists_found) == 1:
                    print("✅ Found exactly one list in response, assuming it's the character list")
                    result = lists_found[0]
                elif len(lists_found) > 1:
                    # Pick the largest list if multiple lists found
                    print(f"✅ Found {len(lists_found)} lists, picking the largest one")
                    result = max(lists_found, key=len)
        
        # One last fallback: if it's still a dict, it might be a dictionary of characters
        if isinstance(result, dict):
            # Check if values look like character objects (have role, arc, etc.)
            first_val = next(iter(result.values())) if result else None
            if isinstance(first_val, dict) and ('role' in first_val or 'arc' in first_val):
                print("✅ Found dictionary of characters, converting to list")
                # Ensure each character has a name key
                result_list = []
                for name, data in result.items():
                    if isinstance(data, dict):
                        char_obj = data.copy()
                        if 'name' not in char_obj:
                            char_obj['name'] = name
                        result_list.append(char_obj)
                result = result_list
        
        if not isinstance(result, list):
            raise ValueError(f"AI returned {type(result).__name__} instead of a list. Keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
            
        return result
        
    except Exception as e:
        print(f"❌ Character generation error: {e}")
        if 'response' in locals() and response:
            print(f"Full response for debugging: {response}")
        raise Exception(f"Failed to generate characters: {str(e)}")
