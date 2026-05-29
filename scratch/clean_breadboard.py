from PIL import Image
import numpy as np

img_bak = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\conexion_nodo_ambiente_1779985459934.png"

with Image.open(img_bak) as im:
    im = im.convert("RGB")
    dest = im.copy()
    
    # We want to find a clean vertical slice of the breadboard (e.g. rows A-J, columns 6-10)
    # Let's inspect x coordinates of column 6 to 10.
    # In Fritzing breadboard:
    # Column 1 is around x = 300? No, let's find it.
    # Let's crop a column and check if it's clean.
    # Actually, we can just copy column 10 to 14, which is in the region x = 200 to 290.
    # Let's see if the breadboard in the range x=180 to 280, y=250 to 580 has wires.
    # In the original, DHT11 wires go down at x=145, 163. The breadboard at x=180 to 280 is completely clean!
    # Let's copy a clean slice of the breadboard from x=200 to 274 (width=74, which is exactly 4 columns).
    # And we can paste it to clean the areas where wires are!
    clean_slice = im.crop((200, 250, 274, 580))
    clean_slice.save("breadboard_clean_slice.png")
    print("Saved clean breadboard slice.")
