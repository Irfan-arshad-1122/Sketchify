import os
import sys
from app import app, PROJECT_ROOT

def test_system():
    print("\n=== SYSTEM TEST ===")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Uploads folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Outputs folder: {app.config['OUTPUT_FOLDER']}")
    
    # Test imports
    try:
        from sketch_processor import generate_all_sketches
        print("✅ Import test passed")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
    
    # Test folder structure
    folders = [
        app.config['UPLOAD_FOLDER'],
        app.config['OUTPUT_FOLDER']
    ]
    for folder in folders:
        if os.path.exists(folder):
            print(f"✅ Folder exists: {folder}")
        else:
            print(f"❌ Missing folder: {folder}")
            os.makedirs(folder)
            print(f"Created folder: {folder}")

if __name__ == '__main__':
    test_system()