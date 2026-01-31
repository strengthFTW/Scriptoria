"""
Script Analyzer - Analyzes existing scripts to extract structure and generate pre-production materials
"""
import json
from utils.ai_client import get_ai_client
from utils.json_helper import safe_parse_json

def analyze_script(script_text: str, genre: str = "Drama") -> dict:
    """
    Analyze an existing script and extract screenplay structure
    
    Args:
        script_text: Full text of the existing script
        genre: Genre of the script
        
    Returns:
        Dictionary containing screenplay structure data
    """
    client = get_ai_client()
    
    prompt = f"""You are a professional script supervisor analyzing screenplay material (full script, treatment, or outline).

SCRIPT/TREATMENT TEXT:
{script_text}

GENRE: {genre}

INSTRUCTIONS:
- This may be a full screenplay, treatment, outline, or beat sheet
- If character names are provided, use them exactly as written
- If no character names are given, suggest appropriate names based on character descriptions
- Extract structure even from short treatments or outlines
- Expand brief descriptions into fuller narrative descriptions

Return a JSON object with the following format:

{{
    "title": "Extract or infer the title from the script",
    "logline": "Create a compelling one-sentence logline based on the script",
    "genre": "{genre}",
    "mainCharacters": [
        "First main character's name (extracted from script)",
        "Second main character's name (extracted from script)",
        "Third main character's name (extracted from script)"
    ],
    "threeActStructure": {{
        "act1": {{
            "title": "Act 1: Setup",
            "description": "Summarize Act 1 based on the script content",
            "keyEvents": [
                "Key event 1 from the script",
                "Key event 2 from the script",
                "Key event 3 from the script"
            ]
        }},
        "act2": {{
            "title": "Act 2: Confrontation",
            "description": "Summarize Act 2 based on the script content",
            "keyEvents": [
                "Key event 1 from the script",
                "Key event 2 from the script",
                "Key event 3 from the script"
            ]
        }},
        "act3": {{
            "title": "Act 3: Resolution",
            "description": "Summarize Act 3 based on the script content",
            "keyEvents": [
                "Key event 1 from the script",
                "Key event 2 from the script",
                "Key event 3 from the script"
            ]
        }}
    }},
    "plotPoints": [
        "Opening Image (describe from script)",
        "Catalyst (describe from script)",
        "Midpoint (describe from script)",
        "All is Lost (describe from script)",
        "Climax (describe from script)",
        "Resolution (describe from script)"
    ]
}}

IMPORTANT: 
- Extract character names if provided (like "Arjun Rao" or "Detective Arjun")
- If only descriptions are given (like "a detective"), infer appropriate names
- Work with whatever level of detail is provided (full script or brief outline)
- If acts are already labeled (Act I, Act II, Act III), use that structure
- Base all responses on the actual content provided

Return ONLY the JSON object, no additional text."""

    try:
        response = client.generate(prompt, json_mode=True)
        result = safe_parse_json(response)
        
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            raise ValueError(f"AI returned {type(result).__name__} instead of dictionary object")
            
        return result
        
    except Exception as e:
        print(f"❌ Script analysis error: {e}")
        if 'response' in locals() and response:
            print(f"Full response for debugging: {response}")
        raise Exception(f"Failed to analyze script: {str(e)}")


def extract_characters_from_script(script_text: str) -> list:
    """
    Extract character information from script text
    
    Args:
        script_text: Full text of the script
        
    Returns:
        List of character names found in the script
    """
    client = get_ai_client()
    
    prompt = f"""Analyze this script and extract all speaking character names.

SCRIPT:
{script_text}

Return a JSON array of character names (3-5 main characters) in order of importance:
["Character Name 1", "Character Name 2", "Character Name 3"]

Return ONLY the JSON array, no additional text."""

    try:
        response = client.generate(prompt, json_mode=True)
        result = safe_parse_json(response)
        
        if isinstance(result, list):
            return result
        else:
            return []
            
    except Exception as e:
        print(f"❌ Character extraction error: {e}")
        return []
