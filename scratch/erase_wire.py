import os
from PIL import Image, ImageDraw

uploaded_img = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\media__1780053379736.png"

def is_red(pixel):
    r, g, b = pixel[:3]
    return r > 150 and g < 100 and b < 100

def patch_image(img_path, output_path):
    img = Image.open(img_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # 1. Erase the red wire using horizontal interpolation
    for y in range(350, 960):
        # find red segment in this row
        red_start = -1
        red_end = -1
        for x in range(200, 400):
            if is_red(pixels[x, y]):
                if red_start == -1:
                    red_start = x
                red_end = x
        
        if red_start != -1:
            # Get color to the left and right
            left_color = pixels[max(0, red_start - 3), y]
            right_color = pixels[min(width - 1, red_end + 3), y]
            
            # Interpolate
            span = red_end - red_start + 1
            for i in range(span):
                ratio = i / float(span)
                r = int(left_color[0] * (1 - ratio) + right_color[0] * ratio)
                g = int(left_color[1] * (1 - ratio) + right_color[1] * ratio)
                b = int(left_color[2] * (1 - ratio) + right_color[2] * ratio)
                pixels[red_start + i, y] = (r, g, b, 255)
                
    # 2. Draw new orange wire to 3.3v.
    # Where is 3.3v? ESP32 usually has 3V3 at the top left pin.
    # The old red wire connected to VIN. VIN is bottom right or top right?
    # Let's just draw an orange line from the bottom of the old red wire (approx x=250, y=940)
    # to the top left of the ESP32 (approx x=250, y=200). Wait, we don't know the coordinates.
    # Let's save the erased image first so I can inspect or run a quick pass.
    
    img.save(output_path)

if os.path.exists(uploaded_img):
    dest = r"c:\Users\jacob\Downloads\TFG\Documento final\scratch\erased_wire.png"
    patch_image(uploaded_img, dest)
    print("Erased red wire and saved to scratch/erased_wire.png")
