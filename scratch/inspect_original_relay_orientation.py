from PIL import Image
import os

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_bak = os.path.join(backup_dir, "conexion_nodo_ambiente_1779985459934.png")

if os.path.exists(img_bak):
    with Image.open(img_bak) as im:
        # Crop the top area of the relay in original (y=670 to 720)
        # Crop the bottom area of the relay in original (y=920 to 975)
        # We check the color in these regions.
        # Blue casing is (130, 196, 244) or similar.
        # Let's check the colors of the screw terminals (gray-blue, (69, 93, 103))
        # to see if they are at the top or bottom of the relay module.
        top_color_sample = im.getpixel((850, 690))
        bottom_color_sample = im.getpixel((850, 960))
        print("Original image top of relay color (850, 690):", top_color_sample)
        print("Original image bottom of relay color (850, 960):", bottom_color_sample)
        
        # Let's check where the text "Relay Module" or "Songle" was written originally.
        # We can scan the original crop and check if there are white letters at the bottom or top.
else:
    print("Backup image not found.")
