from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")
output_path = "test_tiled_grid.png"

with Image.open(img_bak) as im:
    im = im.convert("RGB")
    # Take a 74x74 tile from empty grid at (900, 150)
    tile = im.crop((900, 150, 974, 224))
    dest = im.copy()
    
    # We want to cover the region x = 740 to 1024, y = 600 to 1024
    # The grid period is 37 pixels. Let's cover with tiles aligned to 37px boundaries relative to the source.
    # Source top-left is (900, 150).
    # Any target paste coordinate (px, py) should satisfy:
    # (px - 900) % 37 == 0 and (py - 150) % 37 == 0
    # Let's loop and paste:
    for px in range(715, 1024, 37):
        for py in range(583, 1024, 37):
            # To be absolutely sure, let's only paste if px and py are in or near our target area
            if px >= 720 and py >= 590:
                dest.paste(tile, (px, py))
                
    dest.save(output_path)
    print("Saved tiled image to", output_path)
