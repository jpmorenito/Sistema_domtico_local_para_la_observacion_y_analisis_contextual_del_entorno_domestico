import os
from PIL import Image

screenshots = [
    "C:/Users/jacob/Pictures/Screenshots/Captura de pantalla 2026-06-01 144847.png",
    "C:/Users/jacob/Pictures/Screenshots/Captura de pantalla 2026-06-01 144855.png",
    "C:/Users/jacob/Pictures/Screenshots/Captura de pantalla 2026-06-01 144912.png",
    "C:/Users/jacob/Pictures/Screenshots/Captura de pantalla 2026-06-01 144927.png"
]

print("Analyzing screenshots...")

# Check if pytesseract is available
has_tesseract = False
try:
    import pytesseract
    # Try running a dummy command to see if the executable is set up
    pytesseract.get_tesseract_version()
    has_tesseract = True
    print("pytesseract is available and configured!")
except Exception as e:
    print(f"pytesseract not fully available: {e}")
    print("We will fall back to reading image sizes/metadata.")

for path in screenshots:
    if os.path.exists(path):
        try:
            img = Image.open(path)
            print(f"\nFile: {os.path.basename(path)}")
            print(f"Size: {img.size} | Format: {img.format} | Bytes: {os.path.getsize(path)}")
            
            if has_tesseract:
                # Extract text
                text = pytesseract.image_to_string(img)
                # print first 300 characters of extracted text
                print("Extracted Text (first 250 chars):")
                print("-" * 40)
                print(text[:250].strip())
                print("-" * 40)
                
                # Check for keywords
                keywords = ["iluminacion", "alarma", "radar", "puerta", "pomodoro", "descanso", "ausencia", "ssr", "rele", "seguridad"]
                found_kw = [kw for kw in keywords if kw in text.lower()]
                print("Keywords found:", found_kw)
        except Exception as e:
            print(f"Error opening {path}: {e}")
    else:
        print(f"File not found: {path}")
