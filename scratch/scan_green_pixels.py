from PIL import Image

esp = Image.open("original_esp32_crop.png")
esp_rgba = esp.convert("RGBA")

green_pixels = []
for x in range(esp_rgba.width):
    for y in range(esp_rgba.height):
        r, g, b, a = esp_rgba.getpixel((x, y))
        # Look for green pin header holes
        if r < 100 and g > 180 and b < 100:
            green_pixels.append((x, y))

print("Found {} green pixels.".format(len(green_pixels)))
# Group by Y and print some sample points
import collections
by_y = collections.defaultdict(list)
for x, y in green_pixels:
    by_y[y].append(x)

# Print sorted Y values with their average X
for y in sorted(by_y.keys()):
    avg_x = sum(by_y[y]) / len(by_y[y])
    print(f"y={y}: avg_x={avg_x:.1f}, count={len(by_y[y])}")
