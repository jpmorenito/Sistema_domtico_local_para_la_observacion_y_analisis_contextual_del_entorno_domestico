import os
from PIL import Image

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
art_dir = os.path.join(backup_dir, "artifacts")

assets = [
    "esp32_unmirrored.png",
    "clean_DHT11_cropped.png",
    "clean_LDR_cropped.png",
    "clean_Sound_cropped.png",
    "clean_Laser_cropped.png",
    "clean_Radar_cropped.png",
    "clean_Reed_cropped.png",
    "clean_background.png"
]

print("Checking assets in artifacts:")
for asset in assets:
    p = os.path.join(art_dir, asset)
    if os.path.exists(p):
        with Image.open(p) as img:
            print(f"Asset: {asset} | Size: {img.size} | Mode: {img.mode}")
    else:
        print(f"Asset: {asset} | NOT FOUND at {p}")
