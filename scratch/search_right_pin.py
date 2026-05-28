from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Scan horizontal range x=875 to 895, y=960 to 972 to find dark pixels (the GND pin)
        print("Scanning for right pin (GND):")
        for y in range(958, 974, 2):
            dark_pixels = []
            for x in range(875, 895):
                r, g, b, *a = im.getpixel((x, y))
                if r < 120 and g < 120 and b < 120:
                    dark_pixels.append((x, (r, g, b)))
            if dark_pixels:
                avg_x = sum(x for x, c in dark_pixels) / len(dark_pixels)
                print(f"  y={y}: found dark pixels at avg_x={avg_x:.1f}, x-coords={[x for x, c in dark_pixels]}")
else:
    print("Backup image not found.")
