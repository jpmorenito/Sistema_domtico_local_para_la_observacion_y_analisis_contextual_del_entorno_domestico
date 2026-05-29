import os
from PIL import Image, ImageDraw, ImageFont

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780050760047.png"
dest_img = r"c:\Users\jacob\Downloads\TFG\Documento final\Img\conexion_nodo_escritorio.png"
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
        draw = ImageDraw.Draw(img)
        
        # We draw clean labels:
        # 1. ESP32 at the top (x=411, y=45)
        font_esp = get_font(28, bold=True)
        draw.text((411, 45), "ESP32", fill="black", font=font_esp, anchor="mm")
        
        # 2. Radar LD2410 at the bottom-left (x=160, y=880)
        font_sensors = get_font(18, bold=True)
        draw.text((160, 880), "Radar LD2410", fill="black", font=font_sensors, anchor="mm")
        
        # 3. Diodo Láser at the bottom-right (x=660, y=880)
        # Note: The laser is at the bottom right. Let's center it below the laser board (around x=660)
        draw.text((660, 880), "Diodo Láser", fill="black", font=font_sensors, anchor="mm")
        
        # Save as RGB to dest_img
        img.convert("RGB").save(dest_img)
        print("Labelled image saved successfully to Img/conexion_nodo_escritorio.png")
else:
    print("Uploaded image not found!")
