import os

filepath = "c:/Users/jacob/Downloads/TFG/Documento final/5_seleccion_tecnologias.tex"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    line_lower = line.lower()
    if "ldr" in line_lower or "fotorresistor" in line_lower or "iluminancia" in line_lower or "dht11" in line_lower:
        print(f"Línea {idx+1}: {line.strip()}")
