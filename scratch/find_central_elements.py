from PIL import Image
import numpy as np

img_path = "c:/Users/jacob/Downloads/TFG/Documento final/Img/Diagramas/diagrama_flujo_fsm.png"
img = Image.open(img_path)
width, height = img.size
gray = img.convert("L")
arr = np.array(gray)

# Busquemos filas con pixeles oscuros en la columna central (X=1573)
# El eje central vertical de la imagen es X ~ 1573
x_center = 1573

# Encontremos dónde están las cajas en Y
# Un pixel es oscuro si su valor es < 200
column = arr[:, x_center]
y_indices = np.where(column < 200)[0]

# Agrupemos índices contiguos para detectar las zonas verticales de los elementos
groups = []
if len(y_indices) > 0:
    current_group = [y_indices[0]]
    for y in y_indices[1:]:
        if y - current_group[-1] <= 5:
            current_group.append(y)
        else:
            groups.append(current_group)
            current_group = [y]
    groups.append(current_group)

print("Grupos verticales detectados en X=1573:")
for i, g in enumerate(groups):
    y_min, y_max = g[0], g[-1]
    # Encontremos la anchura de este elemento buscando a la izquierda y derecha en Y central
    y_mid = (y_min + y_max) // 2
    row = arr[y_mid, :]
    dark_in_row = np.where(row < 240)[0]
    if len(dark_in_row) > 0:
        x_min, x_max = dark_in_row[0], dark_in_row[-1]
    else:
        x_min, x_max = 0, 0
    print(f"Grupo {i}: Y [{y_min}..{y_max}], Alto={y_max-y_min+1}. Caja horizontal estimada: X [{x_min}..{x_max}], Ancho={x_max-x_min+1}")
