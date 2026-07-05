import os

filepath = "c:/Users/jacob/Downloads/TFG/Documento final/5_seleccion_tecnologias.tex"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "hw_ldr" in line or "hw_dht" in line or "hw_sonido" in line:
        print(f"Línea {idx+1}: {line.strip()}")
