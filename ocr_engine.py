import pytesseract
from PIL import Image, ImageOps
import pandas as pd
import re
import io
import cv2
import numpy as np

def preprocess_image(image):
    """
    Converts PIL image to grayscale and applies thresholding
    to make text stand out (dot-matrix fix).
    """
    # Convert PIL to OpenCV format (numpy array)
    img_array = np.array(image)
    
    # Convert to grayscale if not already
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array

    # Apply simple thresholding to binarize the image
    # Values below 150 become 0 (black), above become 255 (white)
    # This helps remove faint noise and strengthens the dot-matrix text
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Optional: Dilate slightly to connect dots in dot-matrix
    # kernel = np.ones((2,2), np.uint8)
    # thresh = cv2.dilate(thresh, kernel, iterations=1)
    
    return Image.fromarray(thresh)

def process_image(image_bytes):
    """
    Takes raw image bytes, converts to image, runs OCR, 
    and returns a pandas DataFrame with columns: 
    FECHA, DESCRIPCION, MONTO, DOCUMENTO
    """
    
    # Load image
    original_image = Image.open(io.BytesIO(image_bytes))
    
    # Preprocess image
    processed_image = preprocess_image(original_image)
    
    # Perform OCR
    # --psm 6: Assume a single uniform block of text.
    # This works best for table-like structures.
    custom_config = r'--psm 6' 
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    
    data = []
    
    # Robust Regex Pattern
    # This searches for:
    # 1. Date+Time: (YYYY-MM-DD HH:mm)
    # 2. Description: Anything in between (lazy match)
    # 3. Amount: Number with decimal (e.g., 4800.00)
    # 4. Document: Integer (e.g., 31571483)
    # 5. It ignores any text after the Document number (like the "0-0 MAESTRIA..." part)
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})\s+(.*?)\s+(\d+\.\d{2})\s+(\d+).*')
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = pattern.match(line)
        if match:
            fecha = match.group(1)
            descripcion = match.group(2).strip()
            monto = match.group(3)
            documento = match.group(4)
            
            data.append({
                "FECHA": fecha,
                "DESCRIPCION": descripcion,
                "MONTO": monto,
                "DOCUMENTO": documento
            })
            
    df = pd.DataFrame(data)
    return df
