from PIL import Image, ImageDraw, ImageFont
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")
img_dest = os.path.join(img_dir, "conexion_nodo_ambiente.png")
debug_path = os.path.join(backup_dir, "relay_debug.png")

font_path = r"C:\Windows\Fonts\arial.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

# Restore original
shutil.copy(img_bak, img_dest)

with Image.open(img_dest) as img:
    draw = ImageDraw.Draw(img)
    bg_white = (255, 255, 255)
    
    # Remove header
    draw.rectangle([0, 0, 1024, 140], fill=bg_white)
    
    # Before cropping, let's analyze the original relay layout
    # Sample colors at various y positions along x=850 (center of relay)
    print("=== Original relay colors at x=850 ===")
    for y in range(670, 980, 10):
        c = img.getpixel((850, y))
        print(f"  y={y}: {c}")
    
    # Also sample horizontally at y=750 (should be casing)
    print("=== Original relay colors at y=750 ===")
    for x in range(785, 920, 5):
        c = img.getpixel((x, 750))
        print(f"  x={x}: {c}")
    
    # Crop relay - save debug
    relay_crop = img.crop((785, 672, 920, 975))
    relay_crop.save(debug_path)
    print(f"\nSaved debug crop to {debug_path}")
    print(f"Crop size: {relay_crop.size}")
