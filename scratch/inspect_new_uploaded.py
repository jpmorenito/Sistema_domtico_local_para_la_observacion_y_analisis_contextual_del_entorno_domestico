import os
from PIL import Image

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780051011106.png"

if os.path.exists(uploaded_img):
    with Image.open(uploaded_img) as img:
        print(f"Newest Uploaded Image Size: {img.size} | Mode: {img.mode}")
else:
    print("Newest uploaded image not found!")
