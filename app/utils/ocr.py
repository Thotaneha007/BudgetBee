import re
from datetime import date
from PIL import Image
import pytesseract

def extract_receipt_data(image_stream):
    try:
        # Load image
        img = Image.open(image_stream)
        
        # Check if tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except pytesseract.TesseractNotFoundError:
            print("-" * 50)
            print("OCR ERROR: Tesseract OCR engine not found on system.")
            print("To use OCR, please install Tesseract OCR:")
            print("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
            print("Linux: sudo apt install tesseract-ocr")
            print("-" * 50)
            # Return some dummy data for demo purposes if tesseract is missing
            return {
                'amount': 450.00,
                'date': date.today().strftime('%Y-%m-%d'),
                'merchant': 'Demo Merchant (Install Tesseract for real OCR)'
            }

        # Use Tesseract to do OCR
        text = pytesseract.image_to_string(img)
        return parse_receipt_text(text)
    except Exception as e:
        print(f"OCR Error: {e}")
        return None

def parse_receipt_text(text):
    data = {
        'amount': None,
        'date': None,
        'merchant': 'Extracted Merchant' # Naive fallback
    }
    
    lines = text.split('\n')
    
    # Try to find the merchant (often the first non-empty line)
    for line in lines:
        if line.strip() and len(line.strip()) > 3:
            data['merchant'] = line.strip()
            break
            
    # Try to find date
    date_pattern = re.compile(r'\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}')
    date_match = date_pattern.search(text)
    if date_match:
        data['date'] = date_match.group()
        
    # Try to find amount (look for currency symbols or "Total" followed by number)
    # Simple regex for finding largest decimal number after word 'total'
    total_pattern = re.compile(r'(?i)total[\s:$]*(\d+\.\d{2})')
    total_match = total_pattern.search(text)
    if total_match:
        data['amount'] = total_match.group(1)
    else:
        # Fallback: find all decimals, take max
        decimals = re.findall(r'\d+\.\d{2}', text)
        if decimals:
            data['amount'] = max([float(d) for d in decimals])
            
    return data
