from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Let's sample the color of the blue relay casing (around x=850, y=780 in original)
        casing_color = im.getpixel((850, 780))
        print("Blue relay casing color:", casing_color)
        
        # Let's also check the screw terminals color (around x=815, y=700 in original)
        terminals_color = im.getpixel((815, 700))
        print("Blue terminals color:", terminals_color)
else:
    print("Backup image not found.")
