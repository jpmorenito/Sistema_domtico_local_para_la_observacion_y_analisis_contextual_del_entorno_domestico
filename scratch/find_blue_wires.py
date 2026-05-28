from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Let's inspect the vertical lines of blue/cyan color.
        # Blue wire color in Fritzing is typically around (25, 100, 150) or similar.
        # Let's scan the whole image for blue wires.
        print("Scanning for blue wires in the original image...")
        width, height = im.size
        # We search for pixels where b > r + 50 and b > g + 20 and b > 100 (blue wire)
        blue_pixels = []
        for y in range(0, height, 10):
            row_blue = []
            for x in range(width):
                r, g, b, *a = im.getpixel((x, y))
                if b > r + 50 and b > g + 20 and b > 100:
                    row_blue.append(x)
            if row_blue:
                print(f"y={y}: x-coords={row_blue}")
else:
    print("Backup image not found.")
