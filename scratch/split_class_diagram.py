import os
from PIL import Image

image_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_clases.png"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas"

if not os.path.exists(image_path):
    print(f"Error: No existe el archivo {image_path}")
    exit(1)

with Image.open(image_path) as img:
    width, height = img.size
    print(f"Dimensiones de diagrama_clases.png: {width}x{height}, format={img.format}, mode={img.mode}")
    
    # Vamos a cortar por la mitad (horizontalmente o verticalmente?)
    # Si están una al lado de la otra, cortamos a la mitad vertical (por el eje X).
    # Izquierda: firmware, Derecha: servidor
    mid_x = width // 2
    
    left_box = (0, 0, mid_x, height)
    right_box = (mid_x, 0, width, height)
    
    left_img = img.crop(left_box)
    right_img = img.crop(right_box)
    
    left_path = os.path.join(output_dir, "diagrama_clases_firmware.png")
    right_path = os.path.join(output_dir, "diagrama_clases_servidor.png")
    
    left_img.save(left_path)
    right_img.save(right_path)
    print(f"Guardado firmware en: {left_path}")
    print(f"Guardado servidor en: {right_path}")
