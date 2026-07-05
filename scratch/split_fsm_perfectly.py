import os
from PIL import Image

image_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_flujo_fsm.png"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas"

if not os.path.exists(image_path):
    print(f"Error: {image_path} no existe")
    exit(1)

with Image.open(image_path) as img:
    # Asegurarnos de trabajar en RGB para pintar de blanco si es necesario
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    width, height = img.size
    print(f"Imagen original: {width} x {height}")
    
    # --- PARTE 1: Ramas izquierdas (Ausente y Ocio) + Cajas Centrales ---
    # Rango X: 0 a 1800
    part1 = img.crop((0, 0, 1800, height))
    part1_pixels = part1.load()
    
    # Pintar de blanco las lineas horizontales que salen hacia la derecha desde el centro
    # Centro en X es aprox 1578. Pintamos desde X=1582 hasta el final (1800)
    white = (255, 255, 255)
    
    # Linea superior (Y=174)
    for y in range(171, 178):
        for x in range(1582, 1800):
            part1_pixels[x, y] = white
            
    # Lineas inferiores (Y=660 e Y=680)
    for y in range(657, 664):
        for x in range(1582, 1800):
            part1_pixels[x, y] = white
            
    for y in range(677, 684):
        for x in range(1582, 1800):
            part1_pixels[x, y] = white
            
    part1_path = os.path.join(output_dir, "diagrama_flujo_fsm_parte1.png")
    part1.save(part1_path)
    print(f"Parte 1 guardada en {part1_path} (dimensiones: {part1.size})")
    
    # --- PARTE 2: Ramas derechas (Estudio y Durmiendo) + Cajas Centrales ---
    # Rango X: 1360 a width (3147)
    part2 = img.crop((1360, 0, width, height))
    part2_pixels = part2.load()
    
    # La columna central original estaba en X=1578.
    # En la Parte 2, la coordenada X correspondiente es 1578 - 1360 = 218.
    # Pintamos de blanco las lineas a la izquierda de la columna central (X=0 en part2 hasta X=214)
    
    # Linea superior (Y=174)
    for y in range(171, 178):
        for x in range(0, 214):
            part2_pixels[x, y] = white
            
    # Lineas inferiores (Y=660 e Y=680)
    for y in range(657, 664):
        for x in range(0, 214):
            part2_pixels[x, y] = white
            
    for y in range(677, 684):
        for x in range(0, 214):
            part2_pixels[x, y] = white
            
    part2_path = os.path.join(output_dir, "diagrama_flujo_fsm_parte2.png")
    part2.save(part2_path)
    print(f"Parte 2 guardada en {part2_path} (dimensiones: {part2.size})")
