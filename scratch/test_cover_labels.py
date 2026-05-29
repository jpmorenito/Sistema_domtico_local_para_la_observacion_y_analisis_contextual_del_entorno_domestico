from PIL import Image, ImageDraw

# Load cropped ESP32
esp = Image.open("original_esp32_crop.png")
draw = ImageDraw.Draw(esp)

# Cover left labels: x from 43 to 68, y from 15 to 385
draw.rectangle([43, 15, 68, 385], fill=(255, 0, 0))

# Cover right labels: x from 272 to 297, y from 15 to 385
draw.rectangle([272, 15, 297, 385], fill=(0, 0, 255))

esp.save("test_covered_labels.png")
print("Saved test_covered_labels.png")
