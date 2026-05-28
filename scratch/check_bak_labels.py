from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_escritorio_1779985482306.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Let's inspect some pixels around (450, 10) to (750, 90)
        # In the original, this area is not purely white, it has the ESP32 module colors
        # Let's check pixel color at (600, 50) which is on the ESP32 text area
        print("Color in backup at (600, 50):", im.getpixel((600, 50)))
        print("Color in backup at (600, 25):", im.getpixel((600, 25)))
        # Let's check the area of the laser (bottom of the image)
        print("Color in backup at (600, 950):", im.getpixel((600, 950)))
