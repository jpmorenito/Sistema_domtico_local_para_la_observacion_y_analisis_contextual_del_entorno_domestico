import os
from PIL import Image

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_escritorio_1779985482306.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as img:
        img = img.convert("RGBA")
        
        # In Fritzing, the background grid has a periodic pattern of 37 pixels.
        # We can extract a clean grid slice from x = 640 to 650 (width=10) and y = 580 to 820
        # and paste it over the red wire at x = 614 to 624 (width=10)
        # Let's inspect if that works.
        clean_slice = img.crop((640, 580, 650, 820))
        img.paste(clean_slice, (614, 580))
        
        # Save a test image to artifacts to see if the erase is clean
        dest_p = os.path.join(backup_dir, "artifacts", "test_laser_wire_erased.png")
        img.convert("RGB").save(dest_p)
        print("Test image saved to artifacts/test_laser_wire_erased.png")
else:
    print("Backup not found!")
