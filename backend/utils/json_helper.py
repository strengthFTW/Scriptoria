"""
Utility for robustly extracting and parsing JSON from AI responses
"""
import json
import re

def extract_json(response: str) -> str:
    """
    Extracts JSON string from a response that might contain markdown or extra text.
    """
    # Clean the response of any weird characters that might break parsing
    # (e.g., hidden control characters)
    response = "".join(char for char in response if ord(char) >= 32 or char in "\n\r\t")
    
    # 1. Look for ```json ... ``` blocks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
    if json_match:
        return json_match.group(1).strip()
    
    # 2. Look for the first '[' or '{' and the last ']' or '}'
    first_bracket = response.find('[')
    first_brace = response.find('{')
    
    start_idx = -1
    if first_bracket != -1 and (first_brace == -1 or first_bracket < first_brace):
        start_idx = first_bracket
        end_char = ']'
    elif first_brace != -1:
        start_idx = first_brace
        end_char = '}'
        
    if start_idx != -1:
        last_idx = response.rfind(end_char)
        if last_idx != -1:
            return response[start_idx:last_idx+1].strip()
            
    return response.strip()

def clean_json_string(json_str: str) -> str:
    """
    Cleans common AI-generated JSON mistakes like trailing commas.
    """
    # Remove trailing commas before closing braces/brackets
    json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
    
    # Fix common mistakes like single quotes being used as property names
    # This is risky but helps with some smaller models
    # Only replace ' if it looks like it's surrounding a key
    # json_str = re.sub(r"'(.*?)':", r'"\1":', json_str)
    
    return json_str

def safe_parse_json(response: str):
    """
    Combines extraction and cleaning to safely parse JSON.
    """
    json_str = extract_json(response)
    cleaned_str = clean_json_string(json_str)
    
    try:
        return json.loads(cleaned_str)
    except json.JSONDecodeError as first_error:
        # One last attempt: remove comments if AI included them (e.g., // some comment)
        very_clean_str = re.sub(r'//.*?\n', '\n', cleaned_str)
        very_clean_str = re.sub(r'/\*.*?\*/', '', very_clean_str, flags=re.DOTALL)
        try:
            return json.loads(very_clean_str)
        except:
            raise first_error
