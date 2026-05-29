import os
from PIL import Image, ImageDraw

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780053379736.png"

def is_red(pixel):
    r, g, b = pixel[:3]
    # Red Fritzing wire core is usually very red, e.g. > 200, g < 100, b < 100
    # Red Fritzing wire border is dark red, e.g. > 100, g < 50, b < 50
    return r > 150 and g < 100 and b < 100

if os.path.exists(uploaded_img):
    img = Image.open(uploaded_img).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # We want to find the red wire connected to the DHT11.
    # DHT11 is at the bottom left. Let's scan x from 0 to 300, y from 400 to 900.
    red_pixels = []
    for x in range(300):
        for y in range(400, height):
            if is_red(pixels[x, y]):
                red_pixels.append((x, y))
                
    if red_pixels:
        min_x = min(p[0] for p in red_pixels)
        max_x = max(p[0] for p in red_pixels)
        min_y = min(p[1] for p in red_pixels)
        max_y = max(p[1] for p in red_pixels)
        print(f"Red pixels found in bounding box: ({min_x}, {min_y}) to ({max_x}, {max_y})")
        print(f"Total red pixels in this area: {len(red_pixels)}")
    else:
        print("No red pixels found in the specified area.")
else:
    print("Image not found")
