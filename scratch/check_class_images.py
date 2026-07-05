import os
from PIL import Image, ImageChops

img1_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_clases_firmware.png"
img2_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_clases_servidor.png"

def autocrop_image(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} no existe")
        return
    
    with Image.open(filepath) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # El color del fondo es blanco (255, 255, 255)
        bg = Image.new(img.mode, img.size, (255, 255, 255))
        diff = ImageChops.difference(img, bg)
        # Añadir un pequeño margen de tolerancia
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        
        if bbox:
            print(f"Imagen {os.path.basename(filepath)} - Dimensiones originales: {img.size}")
            print(f"BBox detectado: {bbox} (márgenes a recortar: Izq {bbox[0]}, Top {bbox[1]}, Der {img.size[0] - bbox[2]}, Bot {img.size[1] - bbox[3]})")
            # Dejar un pequeño margen de seguridad de 10 píxeles
            left = max(0, bbox[0] - 10)
            top = max(0, bbox[1] - 10)
            right = min(img.size[0], bbox[2] + 10)
            bottom = min(img.size[1], bbox[3] + 10)
            
            cropped = img.crop((left, top, right, bottom))
            cropped.save(filepath)
            print(f"Imagen recortada y guardada. Nuevas dimensiones: {cropped.size}")
        else:
            print(f"No se detectaron márgenes para recortar en {os.path.basename(filepath)}")

autocrop_image(img1_path)
autocrop_image(img2_path)
