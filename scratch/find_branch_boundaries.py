from PIL import Image
import numpy as np

img_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_flujo_fsm.png"
img = Image.open(img_path)
width, height = img.size
gray = img.convert("L")
arr = np.array(gray)

# Busquemos los limites de los componentes de las ramas en Y de 180 a 650 (excluyendo las cajas centrales)
# Las cajas centrales estan en X [1365..1791]
# Queremos encontrar el elemento mas a la derecha en las ramas de la izquierda (X < 1365)
# y el elemento mas a la izquierda en las ramas de la derecha (X > 1791)
left_max_x = 0
right_min_x = width

for y in range(180, 650):
    row = arr[y, :]
    dark_indices = np.where(row < 240)[0]
    if len(dark_indices) > 0:
        # Para la parte izquierda (ramas 1 y 2)
        left_dark = [x for x in dark_indices if x < 1360]
        if len(left_dark) > 0:
            left_max_x = max(left_max_x, left_dark[-1])
        
        # Para la parte derecha (ramas 3 y 4)
        right_dark = [x for x in dark_indices if x > 1800]
        if len(right_dark) > 0:
            right_min_x = min(right_min_x, right_dark[0])

print(f"Ramas Izquierda (Ausente + Ocio) extrema derecha X: {left_max_x}")
print(f"Ramas Derecha (Estudio + Durmiendo) extrema izquierda X: {right_min_x}")
print(f"Espacio libre entre las ramas de la izquierda y de la derecha en Y [180..650]: X [{left_max_x + 1} .. {right_min_x - 1}]")
