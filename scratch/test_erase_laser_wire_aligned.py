import os
from PIL import Image

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_escritorio_1779985482306.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as img:
        img = img.convert("RGBA")
        
        # Grid period is 37 pixels.
        # We copy a slice from x = (614 + 37) = 651 to x = (624 + 37) = 661
        # and paste it back to x = 614 to 624.
        # Height is from y = 580 to 805.
        clean_slice = img.crop((651, 580, 661, 805))
        img.paste(clean_slice, (614, 580))
        
        dest_p = os.path.join(backup_dir, "artifacts", "test_laser_wire_erased_aligned.png")
        img.convert("RGB").save(dest_p)
        print("Aligned test image saved to artifacts/test_laser_wire_erased_aligned.png")
else:
    print("Backup not found!")
