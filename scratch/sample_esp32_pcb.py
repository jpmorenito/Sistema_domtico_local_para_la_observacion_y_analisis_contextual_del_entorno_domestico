from PIL import Image
import numpy as np

img = Image.open("original_esp32_crop.png")
arr = np.array(img)

# Let's sample colors on the left label area (around x=40, y=250)
print("Color at x=40, y=250:", img.getpixel((40, 250)))
print("Color at x=50, y=250:", img.getpixel((50, 250)))
print("Color at x=60, y=250:", img.getpixel((60, 250)))

# Let's check the size of the image
print("Image size:", img.size)
