import os
from PIL import Image, ImageDraw, ImageFont

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780062607903.png"
dest_path = r"c:\Users\jacob\Downloads\TFG\Documento final\Img\conexion_nodo_ambiente.png"
font_path = r"C:\Windows\Fonts\arial.ttf"

def get_font(size, bold=False):
    try:
        suffix = "bd" if bold else ""
        path = font_path.replace("arial", f"arial{suffix}") if bold else font_path
        if not os.path.exists(path):
            path = font_path
        return ImageFont.truetype(path, size)
    except IOError:
        return ImageFont.load_default()

if os.path.exists(uploaded_img):
    img = Image.open(uploaded_img).convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Text styles
    font_esp = get_font(30, bold=True)
    font_sensors = get_font(20, bold=True)
    
    # Calculate positions based on visual inspection of 750x839 image
    # ESP32: Top center
    draw.text((width // 2, 40), "ESP32", fill="black", font=font_esp, anchor="mm")
    
    # Big Sound: Left middle (Red module)
    draw.text((140, 520), "Big Sound", fill="black", font=font_sensors, anchor="mm")
    
    # Relé: Left bottom (Blue block)
    draw.text((140, 710), "Relé", fill="black", font=font_sensors, anchor="mm")
    
    # DHT11: Right middle (Blue grid)
    draw.text((630, 520), "Sensor DHT11", fill="black", font=font_sensors, anchor="mm")
    
    # LDR: Right bottom (Small black board) - Moved further down and renamed
    draw.text((630, 780), "Fotorresistor", fill="black", font=font_sensors, anchor="mm")
    
    img.convert("RGB").save(dest_path)
    print("Labels applied with correct positions and saved to Img/conexion_nodo_ambiente.png.")
else:
    print(f"Error: {uploaded_img} not found!")
