"""
Screenplay Generator using Gemini API
Generates screenplay outlines with 3-act structure
"""
import json
import re
from utils.ai_client import get_ai_client
from utils.json_helper import safe_parse_json

def generate_screenplay(story_idea: str, genre: str) -> dict:
    """
    Generate screenplay outline from story idea using AI
    
    Args:
        story_idea: User's story concept
        genre: Selected genre
        
    Returns:
        Dictionary containing screenplay data
    """
    client = get_ai_client()
    
    prompt = f"""You are a professional screenplay consultant. Create a compelling screenplay outline based on this story idea.

Story Idea: {story_idea}
Genre: {genre}

IMPORTANT: Define clear character names in your outline and use them consistently throughout all acts. Do NOT use generic names like "protagonist" or "the hero" - give them actual names.

Generate a screenplay outline in the following JSON format. Be creative and detailed:

{{
    "title": "A creative, compelling title for this story",
    "logline": "One powerful sentence that captures the essence of the story",
    "genre": "{genre}",
    "mainCharacters": [
        "First character's full name",
        "Second character's full name",
        "Third character's full name"
    ],
    "threeActStructure": {{
        "act1": {{
            "title": "Act 1: Setup",
            "description": "Brief description of Act 1 - USE THE EXACT CHARACTER NAMES from mainCharacters list",
            "keyEvents": [
                "Event 1 - mention characters by their exact names",
                "Event 2 - mention characters by their exact names",
                "Event 3 - mention characters by their exact names"
            ]
        }},
        "act2": {{
            "title": "Act 2: Confrontation",
            "description": "Brief description of Act 2 - USE THE EXACT CHARACTER NAMES from mainCharacters list",
            "keyEvents": [
                "Event 1 - mention characters by their exact names",
                "Event 2 - mention characters by their exact names",
                "Event 3 - mention characters by their exact names"
            ]
        }},
        "act3": {{
            "title": "Act 3: Resolution",
            "description": "Brief description of Act 3 - USE THE EXACT CHARACTER NAMES from mainCharacters list",
            "keyEvents": [
                "Event 1 - mention characters by their exact names",
                "Event 2 - mention characters by their exact names",
                "Event 3 - mention characters by their exact names"
            ]
        }}
    }},
    "plotPoints": [
        "Opening Image",
        "Catalyst",
        "Midpoint",
        "All is Lost",
        "Climax",
        "Resolution"
    ]
}}

Return ONLY the JSON object, no additional text."""

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
