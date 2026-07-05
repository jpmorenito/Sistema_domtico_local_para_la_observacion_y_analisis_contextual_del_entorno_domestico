with open("c:/Users/jacob/Downloads/TFG/Documento final/__memoria.aux", "r", encoding="utf-8") as f:
    lines = f.readlines()

labels = [
    "fig:conexion_ambiente_diseno",
    "fig:conexion_escritorio_diseno",
    "fig:conexion_puerta_diseno",
    "fig:foto_nodo1",
    "fig:foto_nodo2",
    "fig:foto_nodo3"
]

for line in lines:
    for lbl in labels:
        if lbl in line:
            print(line.strip())
