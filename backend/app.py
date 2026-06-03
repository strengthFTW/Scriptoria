from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os
import io
from datetime import datetime, timedelta


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'dist'))

# Load environment variables
load_dotenv()

# Import generators
from generators.screenplay_generator import generate_screenplay
from generators.character_generator import generate_characters
from generators.scene_generator import generate_scenes
from generators.sound_design_generator import generate_sound_design
from generators.script_analyzer import analyze_script
from utils.pdf_generator import generate_pdf
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx, clean_text

# Import auth and models (User/Story models can stay for backend DB access if needed)
from models import db, bcrypt

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///scriptoria.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Enhanced CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

@app.route('/')
def home():
    """Serve the frontend in production, otherwise show API status."""
    index_path = os.path.join(FRONTEND_DIST_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIST_DIR, 'index.html')

    return jsonify({
        "message": "🎬 Scriptoria Backend API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/generate": "Generate screenplay (POST)",
            "/analyze_script": "Analyze existing script (POST)",
            "/upload": "Upload script file (POST)",
            "/export_pdf": "Export to PDF (POST)"
        }
    })


@app.route('/<path:path>')
def spa_fallback(path):
    """Serve frontend assets and support React Router refreshes."""
    # List of all backend API routes — return 404 for these if not matched above
    API_ROUTES = ('generate', 'analyze_script', 'export_pdf', 'upload', 'health', 'auth')
    if path.split('/')[0] in API_ROUTES:
        return jsonify({"error": "Not found"}), 404

    # Try to serve a static asset (js, css, images, etc.)
    asset_path = os.path.join(FRONTEND_DIST_DIR, path)
    if os.path.exists(asset_path) and os.path.isfile(asset_path):
        return send_from_directory(FRONTEND_DIST_DIR, path)

    # Fallback to index.html for React Router client-side routing
    index_path = os.path.join(FRONTEND_DIST_DIR, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIST_DIR, 'index.html')

    return jsonify({"error": "Frontend not built. Run: cd frontend && npm install && npm run build"}), 404

@app.route('/generate', methods=['POST'])
# @jwt_required()  # Temporarily disabled for testing
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

@app.route('/analyze_script', methods=['POST'])
# @jwt_required()  # Temporarily disabled for testing
def analyze_script_endpoint():
    """
    Analyze an existing script and generate pre-production materials
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        script_text = data.get('scriptText', '').strip()
        genre = data.get('genre', 'Drama')
        
        # Validation
        if not script_text:
            return jsonify({
                "success": False,
                "error": "Script text is required"
            }), 400
        
        if len(script_text) < 100:
            return jsonify({
                "success": False,
                "error": "Script text is too short (minimum 100 characters)"
            }), 400
        
        if len(script_text) > 100000:
            return jsonify({
                "success": False,
                "error": "Script text is too long (maximum 100,000 characters)"
            }), 400
        
        print(f"🎬 Analyzing existing script...")
        print(f"📝 Genre: {genre}")
        print(f"📄 Script length: {len(script_text)} characters")
        
        # Analyze script using AI
        print("⏳ Analyzing script structure...")
        screenplay_data = analyze_script(script_text, genre)
        print("✅ Script analyzed!")
        
        # Generate characters using AI
        print("⏳ Generating character profiles...")
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
        print(f"❌ Script analysis error: {error_msg}")
        return jsonify({
            "success": False,
            "error": "Failed to analyze script. Please try again.",
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
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    # Check API key
    if os.getenv('GROQ_API_KEY'):
        print("🤖 Groq API key detected")
    else:
        print("⚠️  WARNING: GROQ_API_KEY not found in .env file")
        print("💡 Create a .env file with your API key to enable AI generation")
    
    # Check JWT secret
    if not os.getenv('JWT_SECRET_KEY'):
        print("⚠️  WARNING: Using default JWT_SECRET_KEY (insecure for production)")
        print("💡 Add JWT_SECRET_KEY to .env file for production")
    
    app.run(debug=True, port=5000)
