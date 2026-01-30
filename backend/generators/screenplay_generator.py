"""
Screenplay Generator using Gemini API
Generates screenplay outlines with 3-act structure
"""
import json
import re
from utils.ai_client import get_ai_client

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

Generate a screenplay outline in the following JSON format. Be creative and detailed:

{{
    "title": "A creative, compelling title for this story",
    "logline": "One powerful sentence that captures the essence of the story",
    "genre": "{genre}",
    "threeActStructure": {{
        "act1": {{
            "title": "Act 1: Setup",
            "description": "Brief description of Act 1",
            "keyEvents": [
                "Event 1",
                "Event 2",
                "Event 3"
            ]
        }},
        "act2": {{
            "title": "Act 2: Confrontation",
            "description": "Brief description of Act 2",
            "keyEvents": [
                "Event 1",
                "Event 2",
                "Event 3"
            ]
        }},
        "act3": {{
            "title": "Act 3: Resolution",
            "description": "Brief description of Act 3",
            "keyEvents": [
                "Event 1",
                "Event 2",
                "Event 3"
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
        
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            json_str = json_match.group(0) if json_match else response
        
        screenplay_data = json.loads(json_str)
        return screenplay_data
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response: {response[:200]}...")
        raise Exception("Failed to parse AI response as JSON")
    except Exception as e:
        print(f"❌ Generation error: {e}")
        raise
