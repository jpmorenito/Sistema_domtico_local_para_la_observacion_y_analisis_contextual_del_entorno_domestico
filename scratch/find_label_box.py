from PIL import Image
import numpy as np

img = Image.open("original_esp32_crop.png")
# Let's find white/grey pixels (r > 150, g > 150, b > 150) that represent labels.
# Left side labels should be around x=40 to 80.
# Right side labels should be around x=260 to 300.
# Let's count white pixels in each column.

for x in range(img.width):
    white_count = 0
    for y in range(20, 380):
        r, g, b = img.getpixel((x, y))[:3]
        if r > 180 and g > 180 and b > 180:
            white_count += 1
    if white_count > 10:
        print(f"Column x={x}: {white_count} label/metal pixels")
