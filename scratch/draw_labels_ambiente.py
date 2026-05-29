import os
from PIL import Image, ImageDraw, ImageFont

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780053379736.png"
dest_img = r"c:\Users\jacob\Downloads\TFG\Documento final\Img\conexion_nodo_ambiente.png"
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
    with Image.open(uploaded_img) as img:
        img = img.convert("RGBA")
        width, height = img.size
        draw = ImageDraw.Draw(img)
        
        # 1. ESP32 at the top
        font_esp = get_font(32, bold=True)
        draw.text((width // 2, 40), "ESP32", fill="black", font=font_esp, anchor="mm")
        
        font_sensors = get_font(22, bold=True)
        
        # 2. Sensor DHT11 (bottom left) - Moved even higher
        draw.text((120, height - 250), "Sensor DHT11", fill="black", font=font_sensors, anchor="mm")
        
        # 3. LDR (bottom center)
        draw.text((320, height - 20), "LDR", fill="black", font=font_sensors, anchor="mm")
        
        # 4. Relé (bottom right)
        draw.text((width - 150, height - 20), "Relé", fill="black", font=font_sensors, anchor="mm")
        
        # 5. Big Sound (middle right) - placed even higher
        draw.text((width - 120, height - 430), "Big Sound", fill="black", font=font_sensors, anchor="mm")
        
        # Save as RGB to dest_img
        img.convert("RGB").save(dest_img)
        print("Labelled image saved successfully to Img/conexion_nodo_ambiente.png")
else:
    print("Uploaded image not found!")
