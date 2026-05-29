from PIL import Image
import numpy as np

# Load original relay module
im_relay = Image.open("Img/rele_modulo.png").convert("RGBA")
# Crop based on non-white area
# cmin: 145 rmin: 322 cmax: 932 rmax: 739
crop = im_relay.crop((145, 322, 932, 739))

# Convert white background to transparent
# We'll check if R > 240, G > 240, B > 240
data = np.array(crop)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
white_mask = (r > 240) & (g > 240) & (b > 240)
data[white_mask, 3] = 0  # make transparent

transparent_crop = Image.fromarray(data)

# Rotate 90 degrees CCW (so right side pins go to the top)
rotated = transparent_crop.rotate(90, expand=True)

# Save the rotated transparent image
rotated.save("relay_rotated_transparent.png")
print("Rotated size:", rotated.size)
