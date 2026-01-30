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
        response = client.generate(prompt)
        return safe_parse_json(response)
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response: {response[:500]}...")
        raise Exception("Failed to parse AI response as JSON")
    except Exception as e:
        print(f"❌ Generation error: {e}")
        raise
