import os
from PIL import Image

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780062607903.png"

if os.path.exists(uploaded_img):
    img = Image.open(uploaded_img)
    print(f"Image size: {img.size}")
