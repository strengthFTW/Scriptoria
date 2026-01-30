"""
Sound Design Generator using Groq API
Generates sound design suggestions based on scenes and genre
"""
import json
import re
from utils.ai_client import get_ai_client
from utils.json_helper import safe_parse_json

def generate_sound_design(screenplay_data: dict, scenes: list) -> dict:
    """
    Generate sound design suggestions from screenplay and scenes
    
    Args:
        screenplay_data: Screenplay outline dictionary
        scenes: List of scene dictionaries
        
    Returns:
        Sound design dictionary with music, sfx, and ambience
    """
    client = get_ai_client()
    
    # Type Guard: Ensure inputs are valid
    if not isinstance(screenplay_data, dict):
        raise ValueError("Sound generator received invalid screenplay data.")
    if not isinstance(scenes, list):
        raise ValueError("Sound generator received invalid scene data.")
    
    title = screenplay_data.get('title', 'Untitled')
    genre = screenplay_data.get('genre', 'Drama')
    
    # Extract key scene info
    scene_summary = []
    for scene in scenes[:5]:  # Use first 5 scenes for context
        scene_summary.append(f"Scene {scene.get('sceneNumber')}: {scene.get('location')} - {scene.get('action', '')[:80]}")
    
    prompt = f"""You are a professional sound designer for films. Based on this screenplay, create comprehensive sound design suggestions.

Title: {title}
Genre: {genre}

Key Scenes:
{chr(10).join(scene_summary)}

Generate sound design in this JSON format:

{{
    "musicTheme": {{
        "style": "Musical style/genre for the score",
        "mood": "Overall emotional tone",
        "instruments": ["instrument1", "instrument2", "instrument3"],
        "references": ["Similar film/composer 1", "Similar film/composer 2"]
    }},
    "soundEffects": [
        {{
            "category": "Category (e.g., Environmental, Action, Emotional)",
            "description": "Specific sound effect description",
            "scenes": [1, 2, 3]
        }}
    ],
    "ambience": [
        {{
            "location": "Location type",
            "description": "Ambient sound description",
            "mood": "Emotional quality"
        }}
    ],
    "keyMoments": [
        {{
            "scene": 1,
            "moment": "Description of key moment",
            "soundDesign": "Specific sound design approach"
        }}
    ]
}}

Create detailed, production-ready sound design suggestions. Return ONLY the JSON object, no additional text."""

    try:
        response = client.generate(prompt, json_mode=True)
        result = safe_parse_json(response)
        
        if not isinstance(result, dict):
            raise ValueError(f"AI returned {type(result).__name__} instead of a dictionary for sound design.")
            
        return result
        
    except Exception as e:
        print(f"❌ Sound design generation error: {e}")
        if 'response' in locals() and response:
            print(f"Full response for debugging: {response}")
        raise Exception(f"Failed to generate sound design: {str(e)}")
