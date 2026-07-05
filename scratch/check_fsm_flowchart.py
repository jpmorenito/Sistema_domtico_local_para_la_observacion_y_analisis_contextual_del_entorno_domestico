import os
from PIL import Image

image_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_flujo_fsm.png"

if not os.path.exists(image_path):
    print(f"Error: {image_path} no existe")
    exit(1)

with Image.open(image_path) as img:
    width, height = img.size
    print(f"Dimensiones de diagrama_flujo_fsm.png: {width}x{height}")
