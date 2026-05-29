import os
from PIL import Image

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"

backups = [
    "conexion_nodo_ambiente_1779985459934.png",
    "conexion_nodo_escritorio_1779985482306.png",
    "conexion_nodo_puerta_1779985504271.png"
]

print("Checking backup images:")
for b in backups:
    p = os.path.join(backup_dir, b)
    if os.path.exists(p):
        with Image.open(p) as img:
            print(f"{b}: size={img.size}, mode={img.mode}")
    else:
        print(f"{b}: NOT FOUND")
