from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Sample PCB color of the relay module
        # The relay board is centered around x=850, y=700-900.
        # Let's check color at x=830, y=850 (on the green/blue PCB background)
        pcb_color = im.getpixel((830, 850))
        print("PCB background color of the relay:", pcb_color)
else:
    print("Backup image not found.")
