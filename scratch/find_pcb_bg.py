from PIL import Image
import numpy as np

img = Image.open("original_esp32_crop.png")
arr = np.array(img)

# Let's find dark pixels (r < 40, g < 40, b < 40) on the PCB area (x=10 to 330, y=10 to 390)
dark_pixels = []
for x in range(10, 330):
    for y in range(10, 390):
        r, g, b = img.getpixel((x, y))[:3]
        if r < 45 and g < 45 and b < 45:
            dark_pixels.append((r, g, b))

print("Found", len(dark_pixels), "dark pixels.")
if dark_pixels:
    unique_colors, counts = np.unique(dark_pixels, axis=0, return_counts=True)
    sorted_idx = np.argsort(-counts)
    print("Most common dark colors on the ESP32 board:")
    for idx in sorted_idx[:10]:
        print(f"  Color: {unique_colors[idx]} | Count: {counts[idx]}")
