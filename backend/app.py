from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
import io
from datetime import datetime

# Load environment variables
load_dotenv()

# Import generators
from generators.screenplay_generator import generate_screenplay
from generators.character_generator import generate_characters
from generators.scene_generator import generate_scenes
from generators.sound_design_generator import generate_sound_design
from utils.pdf_generator import generate_pdf
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx, clean_text

app = Flask(__name__)

# Enhanced CORS configuration for production
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

@app.route('/')
def home():
    """Root endpoint to verify backend is running"""
    return jsonify({
        "message": "🎬 Scriptoria Backend API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/generate": "Generate screenplay (POST)",
            "/upload": "Upload script file (POST)",
            "/export_pdf": "Export to PDF (POST)"
        }
    })

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
        
        # Generate scenes using AI
        print("⏳ Generating scene breakdown...")
        scenes = generate_scenes(screenplay_data, characters)
        print("✅ Scenes generated!")
        
        # Generate sound design using AI
        print("⏳ Generating sound design...")
        sound_design = generate_sound_design(screenplay_data, scenes)
        print("✅ Sound design generated!")
        
        response = {
            "success": True,
            "screenplay": screenplay_data,
            "characters": characters,
            "scenes": scenes,
            "soundDesign": sound_design,
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

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    """
    Export screenplay package to PDF
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        pdf_buffer = generate_pdf(data)
        
        filename = f"Scriptoria_{data['screenplay'].get('title', 'Script')}.pdf"
        filename = "".join(x for x in filename if x.isalnum() or x in "._- ")
        
        # Get the PDF size for Content-Length header
        pdf_buffer.seek(0, 2)  # Seek to end
        pdf_size = pdf_buffer.tell()
        pdf_buffer.seek(0)  # Seek back to start
        
        response = send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
        # Add explicit headers to prevent network errors
        response.headers['Content-Length'] = str(pdf_size)
        response.headers['Cache-Control'] = 'no-cache'
        
        return response
    except Exception as e:
        print(f"❌ PDF Export error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and extract text."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = file.filename.lower()
        try:
            file_stream = io.BytesIO(file.read())
            
            if filename.endswith('.pdf'):
                raw_text = extract_text_from_pdf(file_stream)
            elif filename.endswith(('.doc', '.docx')):
                raw_text = extract_text_from_docx(file_stream)
            else:
                return jsonify({"error": "Unsupported file format. Please upload PDF or DOCX."}), 400
            
            extracted_text = clean_text(raw_text)
            
            if len(extracted_text) < 20:
                return jsonify({"error": "Extracting text failed or content too short (min 20 chars)."}), 400
            
            return jsonify({
                "success": True,
                "extracted_text": extracted_text[:2000],  # Limit to 2000 chars for safety
                "full_length": len(extracted_text)
            })
            
        except Exception as e:
            print(f"❌ Upload error: {str(e)}")
            return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

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
