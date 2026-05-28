from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")
output_path = os.path.join(backup_dir, "rotated_relay_test.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Crop the relay board (x=790 to 915, y=672 to 975)
        # Note: Let's expand slightly if needed, e.g. x=785 to 920, y=672 to 975
        relay_crop = im.crop((785, 672, 920, 975))
        # Rotate 180 degrees
        rotated = relay_crop.rotate(180)
        rotated.save(output_path)
        print(f"Rotated relay crop saved to {output_path}")
        print("Size of crop:", relay_crop.size)
else:
    print("Backup image not found.")
