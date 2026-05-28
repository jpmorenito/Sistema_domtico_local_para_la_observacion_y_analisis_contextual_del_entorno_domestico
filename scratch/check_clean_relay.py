from PIL import Image
import os

img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"
rele_path = os.path.join(img_dir, "rele_modulo.png")

if os.path.exists(rele_path):
    with Image.open(rele_path) as im:
        print(f"rele_modulo.png: size={im.size}, mode={im.mode}, format={im.format}")
else:
    print("rele_modulo.png not found")
