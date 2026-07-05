from PIL import Image
import numpy as np

img_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_flujo_fsm.png"
img = Image.open(img_path)
width, height = img.size
print(f"Dimensiones de la imagen: {width} x {height}")

# Convertimos a escala de grises y analizamos filas y columnas
gray = img.convert("L")
arr = np.array(gray)

# Busquemos los píxeles oscuros (líneas y texto tienen valores bajos, el fondo es blanco ~ 255)
# Calculemos el promedio o suma por columnas para ver las zonas vacías
col_sums = np.sum(arr < 240, axis=0)

# Busquemos el espacio vacío entre la rama 2 (Ocio) y la rama 3 (Estudio)
# La rama 2 termina y la rama 3 empieza en la mitad
# Analicemos la columna central y busquemos regiones con pocos píxeles oscuros
center_start = int(width * 0.45)
center_end = int(width * 0.55)

for x in range(center_start, center_end, 10):
    print(f"X={x}: pixeles oscuros = {col_sums[x]}")
