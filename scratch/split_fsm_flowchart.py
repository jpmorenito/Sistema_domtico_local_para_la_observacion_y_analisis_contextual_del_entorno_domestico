import os
from PIL import Image
import numpy as np

image_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_flujo_fsm.png"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas"

if not os.path.exists(image_path):
    print(f"Error: {image_path} no existe")
    exit(1)

with Image.open(image_path) as img:
    width, height = img.size
    gray = img.convert("L")
    arr = np.array(gray)
    
    # Identificar píxeles oscuros (umbral 240)
    binary = (arr > 240).astype(int)
    dark_pixels = np.sum(1 - binary, axis=0)
    
    # Buscar en la zona del 45% al 55%
    start_x = int(width * 0.45)
    end_x = int(width * 0.55)
    
    search_range = dark_pixels[start_x:end_x]
    min_val = np.min(search_range)
    # Encontrar todas las columnas que tienen el valor mínimo
    min_indices = np.where(search_range == min_val)[0]
    # Tomar la del medio de los mínimos
    best_idx = min_indices[len(min_indices) // 2]
    split_x = start_x + best_idx
    
    print(f"Búsqueda entre X={start_x} y X={end_x}")
    print(f"Columna de corte seleccionada en X={split_x} con {dark_pixels[split_x]} píxeles oscuros (mínimo en el rango: {min_val})")
    
    # Guardar las partes
    part1 = img.crop((0, 0, split_x, height))
    part2 = img.crop((split_x, 0, width, height))
    
    part1_path = os.path.join(output_dir, "diagrama_flujo_fsm_parte1.png")
    part2_path = os.path.join(output_dir, "diagrama_flujo_fsm_parte2.png")
    
    part1.save(part1_path)
    part2.save(part2_path)
    
    print(f"Guardada parte 1 en: {part1_path} (dimensiones: {part1.size})")
    print(f"Guardada parte 2 en: {part2_path} (dimensiones: {part2.size})")
