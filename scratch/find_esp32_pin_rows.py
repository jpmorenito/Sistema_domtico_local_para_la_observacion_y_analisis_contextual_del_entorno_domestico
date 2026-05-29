from PIL import Image
import numpy as np

img_bak = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\conexion_nodo_ambiente_1779985459934.png"

with Image.open(img_bak) as im:
    im = im.convert("RGB")
    arr = np.array(im)
    
    # We inspect a vertical line corresponding to breadboard holes or pins.
    # Let's check a column near the ESP32 left edge.
    # In Fritzing breadboard, holes are spaced by exactly 18.5 pixels!
    # Let's find the y-coordinates of the holes.
    # Let's scan y from 200 to 580 and find where it is darkest or has a specific pattern.
    y_start, y_end = 200, 580
    profile = np.mean(arr[y_start:y_end, 338, :], axis=-1)
    
    # Simple peak finder:
    peaks = []
    for i in range(1, len(profile)-1):
        if profile[i] < profile[i-1] and profile[i] < profile[i+1]:
            # check depth
            if profile[i] < 240:
                peaks.append(y_start + i)
                
    # Filter peaks to only those that are roughly spaced by multiples of 18.5 (e.g. 18 or 19)
    filtered_peaks = []
    for p in peaks:
        if not filtered_peaks or abs(p - filtered_peaks[-1]) >= 15:
            filtered_peaks.append(p)
            
    print("Detected pin rows (y coordinates):", filtered_peaks)
    print("Number of detected rows:", len(filtered_peaks))
