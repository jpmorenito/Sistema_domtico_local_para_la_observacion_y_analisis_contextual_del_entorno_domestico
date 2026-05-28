from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")
output_path = os.path.join(backup_dir, "relay_bottom_crop.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Crop the bottom area of the relay module
        relay_bottom = im.crop((790, 890, 920, 990))
        relay_bottom.save(output_path)
        print(f"Relay bottom cropped and saved to {output_path}")
        print("Cropped image size:", relay_bottom.size)
        
        # Let's inspect rows around y=940-985 to find the three pins
        # Pins in Fritzing are typically small circles or metal header rectangles.
        # Let's look for metal colors (like yellow, orange, gray, or copper)
        # or wires that might be connected there. Wait, there are no wires connected there,
        # so we will see the silver/gold color of the pins!
        # Silver/gold pins usually have high values in R, G, B.
        # Let's search for the pin centers by printing color information of the three pins.
        # In the cropped image, the labels are VCC, IN, GND.
        # Let's find where the pins are.
else:
    print("Backup image not found.")
