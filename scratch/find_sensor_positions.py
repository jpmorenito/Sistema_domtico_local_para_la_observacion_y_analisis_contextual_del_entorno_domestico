from PIL import Image
import numpy as np

img_bak = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\conexion_nodo_ambiente_1779985459934.png"

with Image.open(img_bak) as im:
    im = im.convert("RGB")
    arr = np.array(im)
    
    # Check y range from 720 to 970 (where the sensor bodies actually are)
    body_part = arr[720:970, :, :]
    non_bg = (body_part[:, :, 0] < 240) | (body_part[:, :, 1] < 240) | (body_part[:, :, 2] < 240)
    non_bg_count = np.sum(non_bg, axis=0)
    
    in_sensor = False
    start_col = 0
    for x in range(len(non_bg_count)):
        # Sensor bodies are wide and solid, so they will have many non-white pixels per column
        if non_bg_count[x] > 100:
            if not in_sensor:
                in_sensor = True
                start_col = x
        else:
            if in_sensor:
                in_sensor = False
                print(f"Sensor body column range: {start_col} to {x} (width: {x - start_col})")
                
    if in_sensor:
        print(f"Sensor body column range: {start_col} to {len(non_bg_count)} (width: {len(non_bg_count) - start_col})")
