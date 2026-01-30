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
        return safe_parse_json(response)
        
    except Exception as e:
        print(f"❌ Character generation error: {e}")
        if 'response' in locals() and response:
            print(f"Full response for debugging: {response}")
        raise Exception(f"Failed to generate characters: {str(e)}")
