from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")
output_path = os.path.join(backup_dir, "relay_crop.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Crop the relay area
        # The relay is at the right side of the breadboard (around x=750 to 920, y=600 to 950)
        relay_crop = im.crop((740, 600, 920, 950))
        relay_crop.save(output_path)
        print(f"Relay cropped and saved to {output_path}")
        print("Cropped image size:", relay_crop.size)
else:
    print("Backup image not found.")
