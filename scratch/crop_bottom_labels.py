from PIL import Image

esp = Image.open("original_esp32_crop.png")

# Crop the bottom portion of the ESP32 (y=300 to 400, x=0 to 340)
bottom_crop = esp.crop((0, 300, 340, 400))
bottom_crop.save("esp32_bottom_labels.png")

print("Saved bottom labels crop.")
