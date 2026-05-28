from PIL import Image
import os

img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"
img_curr = os.path.join(img_dir, "conexion_nodo_ambiente.png")

if os.path.exists(img_curr):
    with Image.open(img_curr) as im:
        # Check pixel colors at y=640 for the three columns
        print("Colors at y=640 in current image:")
        print("  x=815 (Red?):", im.getpixel((815, 640)))
        print("  x=850 (Green?):", im.getpixel((850, 640)))
        print("  x=885 (Black?):", im.getpixel((885, 640)))
else:
    print("Current image not found.")
