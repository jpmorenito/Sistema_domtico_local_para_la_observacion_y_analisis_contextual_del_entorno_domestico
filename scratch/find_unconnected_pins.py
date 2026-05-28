from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Search for red/orange pixels representing unconnected pins in the bottom region
        # (x=800 to 900, y=900 to 985)
        # Fritzing unconnected pins are usually pure red (255, 0, 0) or red-orange (e.g. R > 200, G < 50, B < 50)
        print("Searching for unconnected pins (red squares):")
        for y in range(900, 985):
            for x in range(800, 900):
                r, g, b, *a = im.getpixel((x, y))
                if r > 180 and g < 60 and b < 60:
                    print(f"  y={y}, x={x}: color=({r},{g},{b})")
else:
    print("Backup image not found.")
