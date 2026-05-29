import os
from PIL import Image

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780053379736.png"

def is_red(pixel):
    r, g, b = pixel[:3]
    return r > 150 and g < 100 and b < 100

if os.path.exists(uploaded_img):
    img = Image.open(uploaded_img).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # Get a sample of the background color near the red wire
    bg_colors = []
    for x in range(215, 300):
        for y in range(400, 900):
            p = pixels[x, y]
            if not is_red(p):
                bg_colors.append(p)
    
    # average background color
    if bg_colors:
        avg_r = sum(c[0] for c in bg_colors) // len(bg_colors)
        avg_g = sum(c[1] for c in bg_colors) // len(bg_colors)
        avg_b = sum(c[2] for c in bg_colors) // len(bg_colors)
        print(f"Average background color near wire: ({avg_r}, {avg_g}, {avg_b})")
else:
    print("Image not found")
