from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Import generators
from generators.screenplay_generator import generate_screenplay
from generators.character_generator import generate_characters

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate screenplay and characters using Gemini AI
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        story_idea = data.get('storyIdea', '').strip()
        genre = data.get('genre', 'Drama')
        
        # Validation
        if not story_idea:
            return jsonify({
                "success": False,
                "error": "Story idea is required"
            }), 400
        
        if len(story_idea) < 20:
            return jsonify({
                "success": False,
                "error": "Story idea must be at least 20 characters"
            }), 400
        
        if len(story_idea) > 500:
            return jsonify({
                "success": False,
                "error": "Story idea must be less than 500 characters"
            }), 400
        
        print(f"🎬 Generating screenplay for: {story_idea[:50]}...")
        print(f"📝 Genre: {genre}")
        
        # Generate screenplay using AI
        print("⏳ Calling Groq API for screenplay...")
        screenplay_data = generate_screenplay(story_idea, genre)
        print("✅ Screenplay generated!")
        
        # Generate characters using AI
        print("⏳ Generating characters...")
        characters = generate_characters(screenplay_data)
        print("✅ Characters generated!")
        
        response = {
            "success": True,
            "screenplay": screenplay_data,
            "characters": characters,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except ValueError as e:
        # API key or configuration errors
        error_msg = str(e)
        print(f"❌ Configuration error: {error_msg}")
        return jsonify({
            "success": False,
            "error": "API configuration error. Please check GROQ_API_KEY in .env file",
            "details": error_msg
        }), 500
    
    except Exception as e:
        # General errors
        error_msg = str(e)
        print(f"❌ Generation error: {error_msg}")
        return jsonify({
            "success": False,
            "error": "Failed to generate screenplay. Please try again.",
            "details": error_msg
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    api_key_set = bool(os.getenv('GROQ_API_KEY'))
    return jsonify({
        "status": "healthy",
        "message": "Scriptoria backend is running",
        "ai_configured": api_key_set
    })

if __name__ == '__main__':
    print("🎬 Scriptoria Backend Starting...")
    print("📡 Server running at http://localhost:5000")
    print("✅ CORS enabled for frontend requests")
    
    # Check API key
    if os.getenv('GROQ_API_KEY'):
        print("🤖 Groq API key detected")
    else:
        print("⚠️  WARNING: GROQ_API_KEY not found in .env file")
        print("💡 Create a .env file with your API key to enable AI generation")
    
    app.run(debug=True, port=5000)
