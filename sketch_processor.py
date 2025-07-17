import cv2
import os

def classic_sketch(gray):
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = 255 - blurred
    return cv2.divide(gray, inverted_blur, scale=256.0)

def light_sketch(gray):
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (31, 31), 0)
    inverted_blur = 255 - blurred
    return cv2.divide(gray, inverted_blur, scale=256.0)

def dark_sketch(gray):
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (11, 11), 0)
    inverted_blur = 255 - blurred
    return cv2.divide(gray, inverted_blur, scale=256.0)

def edge_sketch(gray):
    return cv2.Canny(gray, 50, 150)

def generate_all_sketches(input_path, output_folder, unique_id):
    # Verify input exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found at {input_path}")
    
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("Failed to read image (might be corrupted or wrong format)")
    
    # Process image
    image = cv2.resize(image, (600, 600), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sketches = {
        'classic': classic_sketch(gray),
        'light': light_sketch(gray),
        'dark': dark_sketch(gray),
        'edge': edge_sketch(gray)
    }

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save all sketches
    output_files = {}
    for name, img in sketches.items():
        output_path = os.path.join(output_folder, f"{unique_id}_{name}.jpg")
        cv2.imwrite(output_path, img)
        output_files[name] = output_path
    
    return output_files