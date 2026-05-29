import os
from PIL import Image

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
art_dir = os.path.join(backup_dir, "artifacts")

sensors = [
    "clean_DHT11_cropped.png",
    "clean_LDR_cropped.png",
    "clean_Sound_cropped.png",
    "clean_Laser_cropped.png",
    "clean_Radar_cropped.png",
    "clean_Reed_cropped.png",
    "esp32_unmirrored.png"
]

for s in sensors:
    p = os.path.join(art_dir, s)
    if os.path.exists(p):
        with Image.open(p) as img:
            # Get bounding box of non-zero alpha channel
            bbox = img.getbbox()
            print(f"{s}: size={img.size}, bbox={bbox}, mode={img.mode}")
    else:
        print(f"{s}: NOT FOUND")
