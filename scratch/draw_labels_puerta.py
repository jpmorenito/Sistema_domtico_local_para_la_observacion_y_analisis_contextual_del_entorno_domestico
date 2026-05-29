import os
from PIL import Image, ImageDraw, ImageFont

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780051965568.png"
dest_img = r"c:\Users\jacob\Downloads\TFG\Documento final\Img\conexion_nodo_puerta.png"
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
        
        # 2. Sensor Reed at the bottom
        # Let's put it at the bottom, near the right edge, slightly above the absolute bottom
        font_sensors = get_font(24, bold=True)
        draw.text((width - 10, height - 40), "Sensor Reed", fill="black", font=font_sensors, anchor="rm")
        
        # Save as RGB to dest_img
        img.convert("RGB").save(dest_img)
        print("Labelled image saved successfully to Img/conexion_nodo_puerta.png")
else:
    print("Uploaded image not found!")
