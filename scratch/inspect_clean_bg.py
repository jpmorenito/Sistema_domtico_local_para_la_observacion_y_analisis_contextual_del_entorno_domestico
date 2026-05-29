import os
from PIL import Image
import numpy as np

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
bg_path = os.path.join(backup_dir, "artifacts", "clean_background.png")

if os.path.exists(bg_path):
    with Image.open(bg_path) as img:
        print(f"clean_background.png size: {img.size}")
        # Let's check a few pixels to understand the background
        arr = np.array(img)
        unique_colors = np.unique(arr.reshape(-1, arr.shape[-1]), axis=0)
        print(f"Number of unique colors: {len(unique_colors)}")
        # Check if it has a breadboard
        # Usually, a Fritzing breadboard has a beige color like (240, 230, 210) or similar.
        # Let's check the average color in the center (x: 400-600, y: 300-500)
        center_crop = arr[300:500, 400:600]
        mean_color = center_crop.mean(axis=(0, 1))
        print(f"Mean color in center: {mean_color}")
else:
    print("clean_background.png does not exist!")
