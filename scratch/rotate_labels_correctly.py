from PIL import Image

esp = Image.open("original_esp32_crop.png")

# Left labels are just inside the left header pins (x=30 to x=80 in the 340x400 image)
left_labels = esp.crop((35, 10, 75, 370))
left_labels_rot = left_labels.transpose(Image.ROTATE_270)
left_labels_rot.save("left_labels_rotated_correctly.png")

# Right labels are just inside the right header pins (x=260 to x=310 in the 340x400 image)
right_labels = esp.crop((265, 10, 305, 370))
right_labels_rot = right_labels.transpose(Image.ROTATE_90)
right_labels_rot.save("right_labels_rotated_correctly.png")

print("Saved corrected label crops.")
