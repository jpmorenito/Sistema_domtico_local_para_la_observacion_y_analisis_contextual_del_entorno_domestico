from PIL import Image
import os

# Load the cropped original ESP32
esp = Image.open("original_esp32_crop.png")

# The left labels are roughly in x=[20, 50] relative to the cropped ESP32 (width 340, from 342 to 682)
# Wait, the ESP32 is from x=342 to 682. The PCB itself is from x=390 to 630?
# Let's find the exact bounding box of the PCB.
# Let's crop the left column of labels (x=45 to 80 relative to 342, so x=387 to 422 in absolute coordinates)
# and right column (x=260 to 295 relative to 342, so x=602 to 637 in absolute coordinates)
# Let's do it and rotate 90 degrees CW to make them horizontal.

left_labels = esp.crop((40, 10, 85, 370)) # EN to GND/VIN
left_labels_rot = left_labels.transpose(Image.ROTATE_270) # Rotate so we read from top to bottom
left_labels_rot.save("left_labels_rotated.png")

right_labels = esp.crop((255, 10, 300, 370))
right_labels_rot = right_labels.transpose(Image.ROTATE_90)
right_labels_rot.save("right_labels_rotated.png")

print("Saved rotated label crops.")
