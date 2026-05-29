from PIL import Image

esp = Image.open("original_esp32_crop.png")

# Crop the left labels (vertical text between left pins and shield)
left_labels = esp.crop((55, 10, 95, 370))
left_labels_rot = left_labels.transpose(Image.ROTATE_270)
left_labels_rot.save("left_labels_real.png")

# Crop the right labels (vertical text between right pins and shield)
right_labels = esp.crop((245, 10, 285, 370))
right_labels_rot = right_labels.transpose(Image.ROTATE_90)
right_labels_rot.save("right_labels_real.png")

print("Saved real label crops.")
