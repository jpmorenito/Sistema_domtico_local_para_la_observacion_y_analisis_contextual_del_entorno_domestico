import os
from PIL import Image
import numpy as np

image_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_clases.png"
output_dir = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas"

if not os.path.exists(image_path):
    print(f"Error: {image_path} no existe")
    exit(1)

with Image.open(image_path) as img:
    # Convertir a escala de grises y luego a array binario (0 para negro, 1 para blanco)
    # Suponemos fondo blanco (o claro) y líneas oscuras.
    gray = img.convert("L")
    arr = np.array(gray)
    
    # Umbralizar: 1 si es fondo blanco (cerca de 255), 0 si es línea/texto oscuro (menor que 240)
    binary = (arr > 240).astype(int)
    
    # Calcular la suma de píxeles oscuros por columna
    # Cuantos menos píxeles oscuros (valores 0 en binary), más vacía está la columna.
    # Por lo tanto, buscamos columnas donde la suma de (1 - binary) sea mínima.
    dark_pixels_per_column = np.sum(1 - binary, axis=0)
    
    # Queremos buscar el punto de corte en la zona media de la imagen (por ejemplo, entre el 40% y el 70% del ancho)
    width, height = img.size
    start_search = int(width * 0.40)
    end_search = int(width * 0.70)
    
    # Encontrar la columna con la menor cantidad de píxeles oscuros en ese rango
    search_range = dark_pixels_per_column[start_search:end_search]
    min_idx_in_range = np.argmin(search_range)
    optimal_split_x = start_search + min_idx_in_range
    
    print(f"Búsqueda de corte entre X={start_search} y X={end_search}")
    print(f"Punto de corte óptimo encontrado en X={optimal_split_x} con {dark_pixels_per_column[optimal_split_x]} píxeles oscuros")
    
    # Guardar las imágenes con este nuevo punto de corte
    left_box = (0, 0, optimal_split_x, height)
    right_box = (optimal_split_x, 0, width, height)
    
    left_img = img.crop(left_box)
    right_img = img.crop(right_box)
    
    left_path = os.path.join(output_dir, "diagrama_clases_firmware.png")
    right_path = os.path.join(output_dir, "diagrama_clases_servidor.png")
    
    # Opcional: podemos recortar los bordes en blanco sobrantes si es necesario
    left_img.save(left_path)
    right_img.save(right_path)
    
    print(f"Nuevas sub-imágenes guardadas usando X={optimal_split_x} como divisor.")
