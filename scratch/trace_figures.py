import re

filepath = "c:/Users/jacob/Downloads/TFG/Documento final/4_diseno_sistema.tex"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Busquemos todos los begin{figure}, caption, stepcounter, refstepcounter, etc.
lines = content.split("\n")
for idx, line in enumerate(lines):
    if "begin{figure}" in line or "caption" in line or "stepcounter" in line or "refstepcounter" in line:
        print(f"Línea {idx+1}: {line.strip()}")
