from PIL import Image

esp = Image.open("original_esp32_crop.png")
esp_rgba = esp.convert("RGBA")

# Let's find green pixels in the left and right columns.
# The green pins have a specific bright green color.
# Let's scan a vertical line through the left column of pins (around x=28 in the crop)
# and right column (around x=312 in the crop).

left_x = 28
right_x = 312

print("Scanning left pin column (x={}):".format(left_x))
for y in range(esp_rgba.height):
    r, g, b, a = esp_rgba.getpixel((left_x, y))
    # Green pin color is roughly r < 100, g > 150, b < 100
    if r < 120 and g > 160 and b < 120:
        print(f"y={y}: color=({r},{g},{b})")
