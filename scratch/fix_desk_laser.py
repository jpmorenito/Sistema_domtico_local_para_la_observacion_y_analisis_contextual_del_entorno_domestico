from PIL import Image, ImageDraw, ImageFont
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak_name = "conexion_nodo_escritorio_1779985482306.png"
img_bak = os.path.join(backup_dir, img_bak_name)
img_dest = os.path.join(img_dir, "conexion_nodo_escritorio.png")

font_path = r"C:\Windows\Fonts\arial.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

if os.path.exists(img_bak):
    # Restore the backup first
    shutil.copy(img_bak, img_dest)
    print(f"Restored {img_bak_name} to {img_dest}")
    
    with Image.open(img_dest) as img:
        draw = ImageDraw.Draw(img)
        
        # 1. Clear the entire ESP32 header at the top
        draw.rectangle([450, 10, 750, 90], fill="white")
        # Draw only "ESP32"
        font_esp32 = get_font(36)
        draw.text((560, 20), "ESP32", fill="black", font=font_esp32)
        
        # 2. Paint white over "HLK-LD2410C 2ADAR SENSOR" (top-left text)
        draw.rectangle([10, 185, 275, 270], fill="white")
        
        # 3. Paint white over the entire bottom region to clear the old laser text
        draw.rectangle([300, 900, 900, 1024], fill="white")
        # Draw "Diodo Láser" cleanly
        font_laser = get_font(34)
        draw.text((530, 940), "Diodo Láser", fill="black", font=font_laser)
        
        img.save(img_dest)
        print("Successfully corrected Figure 45 (laser label cleaned and VCC wire removed).")
else:
    print("Backup image not found.")
