import os
import sys
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import uuid

# Get the absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_ROOT, 'static', 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(PROJECT_ROOT, 'static', 'outputs')

# Add project root to Python path
sys.path.append(PROJECT_ROOT)

try:
    from sketch_processor import generate_all_sketches
    print("✅ Import successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Python path:", sys.path)
    print("Files in directory:", [f for f in os.listdir(PROJECT_ROOT) if f.endswith('.py')])
    raise


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())[:8]
    filename = secure_filename(f"{unique_id}_{file.filename}")
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)
    
    # Process image
    output_files = generate_all_sketches(input_path, app.config['OUTPUT_FOLDER'], unique_id)
    
    return jsonify({
        'original': f"static/uploads/{filename}",
        'sketches': {
            'classic': f"static/outputs/{unique_id}_classic.jpg",
            'light': f"static/outputs/{unique_id}_light.jpg",
            'dark': f"static/outputs/{unique_id}_dark.jpg",
            'edge': f"static/outputs/{unique_id}_edge.jpg"
        }
    })

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
