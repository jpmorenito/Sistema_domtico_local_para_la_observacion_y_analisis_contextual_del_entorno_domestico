from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

with Image.open(img_bak) as img:
    # Let's sample the red wire at x=815, y=550 (near breadboard)
    red_color = img.getpixel((815, 550))
    # Let's sample the green wire at x=850, y=550
    green_color = img.getpixel((850, 550))
    # Let's sample the black wire at x=886, y=550
    black_color = img.getpixel((886, 550))
    
    print(f"Red wire color: {red_color}")
    print(f"Green wire color: {green_color}")
    print(f"Black wire color: {black_color}")
