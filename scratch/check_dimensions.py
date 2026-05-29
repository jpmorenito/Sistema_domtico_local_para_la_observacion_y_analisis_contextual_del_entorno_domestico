from PIL import Image
import os

img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"
img_path = os.path.join(img_dir, "conexion_nodo_ambiente.png")

with Image.open(img_path) as img:
    print(f"Image format: {img.format}")
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
