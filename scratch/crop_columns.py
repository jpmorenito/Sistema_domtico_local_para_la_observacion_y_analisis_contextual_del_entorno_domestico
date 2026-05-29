from PIL import Image

esp = Image.open("original_esp32_crop.png")

# Crop right side (x=240 to 330, y=0 to 400)
right_column = esp.crop((240, 0, 330, 400))
right_column.save("esp32_right_column.png")

# Crop left side (x=10 to 100, y=0 to 400)
left_column = esp.crop((10, 0, 100, 400))
left_column.save("esp32_left_column.png")

print("Saved left and right column crops.")
