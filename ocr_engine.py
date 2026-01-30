import pytesseract
from PIL import Image
import pandas as pd
import re
import io

def process_image(image_bytes):
    """
    Takes raw image bytes, converts to image, runs OCR, 
    and returns a pandas DataFrame with columns: 
    FECHA, DESCRIPCION, MONTO, DOCUMENTO
    """
    
    # Load image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Perform OCR
    # Using specific configurations for structured text if needed
    # --psm 6Assume a single uniform block of text. 4 is usually good too.
    # But default often works. Let's try default first.
    text = pytesseract.image_to_string(image)
    
    data = []
    
    # Regex pattern to identify the lines
    # Pattern: Date(YYYY-MM-DD) Time(HH:mm) ... Description ... Amount ... Document
    # Example: 2022-09-05 15:08 POSTGRADO FAC.POLITE 4800.00 31571483
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line starts with a date-like pattern
        # YYYY-MM-DD
        if re.match(r'^\d{4}-\d{2}-\d{2}', line):
            parts = line.split()
            
            # We expect at least: Date, Time, Desc(1+), Amount, Doc
            # Min 5 parts
            if len(parts) >= 5:
                fecha_hora = f"{parts[0]} {parts[1]}"
                
                # The last item is Document
                documento = parts[-1]
                
                # The second to last is Monto
                # However, sometimes OCR might split tokens oddly.
                # Let's assume the basic structure holds for this clear printout.
                monto = parts[-2]
                
                # Description is everything in between
                descripcion = " ".join(parts[2:-2])
                
                # Clean up extracted data if necessary
                # e.g. remove non-numeric chars from monto (except dot)
                
                data.append({
                    "FECHA": fecha_hora,
                    "DESCRIPCION": descripcion,
                    "MONTO": monto,
                    "DOCUMENTO": documento
                })
                
    df = pd.DataFrame(data)
    return df
