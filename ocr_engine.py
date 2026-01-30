import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pandas as pd
import re
import io
import cv2
import numpy as np

def preprocess_image(image):
    """
    Improved preprocessing.
    Instead of hard binary thresholding which loses details,
    we use adaptive thresholding and scaling.
    """
    # Convert to OpenCV
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array

    # 1. Resize/Scale up (helps with small dot-matrix text)
    # Scale by 2x
    height, width = gray.shape
    gray = cv2.resize(gray, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)

    # 2. Denoise
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # 3. Adaptive Thresholding (better for varying lighting)
    # transforms to black and white but respects local contrast
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    return Image.fromarray(thresh)

def process_image(image_bytes):
    # Load image
    original_image = Image.open(io.BytesIO(image_bytes))
    
    # Try preprocessing
    # If the user says "carga pero no lee nada", maybe the image is being corrupted by preprocessing.
    # Let's try to pass the UPSCALED image but possibly without aggressive thresholding if Tesseract fails.
    # For now, let's stick to a robust preprocess: Scale + Adaptive Thresh is usually standard.
    processed_image = preprocess_image(original_image)
    
    # Configuration
    # --psm 4: Assume a single column of text of variable sizes. 
    # (6 is uniform block, also good). Let's stick to 6 but allow simpler fallback if needed.
    custom_config = r'--psm 6' 
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    
    data = []
    
    lines = text.split('\n')
    
    # Flexible Parser strategy
    # Instead of one giant Regex, locate anchors.
    
    for line in lines:
        line_str = line.strip()
        if len(line_str) < 10:
            continue
            
        # 1. Find Date (YYYY-MM-DD)
        # We allow small OCR errors (like S instead of 5) but regex needs to be somewhat strict regarding format
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line_str)
        
        # 2. Find Amount (Number with dot: 4800.00)
        # We look for the LAST occurrence of a price-like pattern in the line, 
        # because the DOCUMENT number usually doesn't have a dot.
        amount_matches = list(re.finditer(r'(\d+\.\d{2})', line_str))
        
        if date_match and amount_matches:
            # We have a valid line candidate
            
            # VALIDATION AND FORMATTING
            
            # Date: Convert YYYY-MM-DD to DD/MM/YYYY
            try:
                dt_obj = pd.to_datetime(fecha_str)
                fecha_formatted = dt_obj.strftime('%d/%m/%Y')
            except:
                fecha_formatted = fecha_str

            # Amount: Convert to float for Excel
            try:
                monto_val = float(monto_str)
            except:
                monto_val = 0.0
            
            # Clean up Description
            # Text strictly between Date(end) and Amount(start)
            raw_desc = line_str[date_end:amount_start].strip()
            # Remove Time-like pattern at start (e.g. 15:08)
            raw_desc = re.sub(r'^\d{2}:\d{2}\s+', '', raw_desc)
            descripcion_str = raw_desc.strip()
            
            # DOCUMENT
            # Text immediately after Amount
            amount_end = amount_match.end()
            remaining_text = line_str[amount_end:].strip()
            
            parts_after = remaining_text.split()
            if parts_after:
                documento_str = parts_after[0]
            else:
                documento_str = ""
            
            data.append({
                "FECHA": fecha_formatted,
                "DESCRIPCION": descripcion_str,
                "MONTO": monto_val,
                "DOCUMENTO": documento_str
            })
            
    df = pd.DataFrame(data)
    return df
