from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_esp32_crop.png")
draw = ImageDraw.Draw(img)

# Try to get Arial font
try:
    font = ImageFont.truetype("arial.ttf", 9)
except IOError:
    font = ImageFont.load_default()

# Draw vertical lines and label them
for x in range(0, img.width, 10):
    color = (255, 0, 0) if x % 50 == 0 else (120, 120, 120)
    draw.line([(x, 0), (x, img.height)], fill=color, width=1)
    if x % 20 == 0:
        draw.text((x + 2, 5), str(x), fill=color, font=font)

# Draw horizontal lines
for y in range(0, img.height, 20):
    color = (0, 0, 255) if y % 100 == 0 else (100, 100, 100)
    draw.line([(0, y), (img.width, y)], fill=color, width=1)
    draw.text((5, y + 2), str(y), fill=color, font=font)

img.save("esp32_with_grid.png")
print("Saved esp32_with_grid.png")
