import os

search_dir = "c:/Users/jacob/Downloads/TFG/Documento final"
search_term = "sensor_ldr_modulo" # O algo relacionado con fotorresistor LDR
# Tambien busquemos por "26" o la etiqueta de la figura

for filename in os.listdir(search_dir):
    if filename.endswith(".tex"):
        filepath = os.path.join(search_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            if "sensor_ldr_modulo" in line or "LDR" in line and "figure" in line.lower() or "fig:" in line and "ldr" in line.lower():
                print(f"Encontrado en {filename}:{idx+1}: {line.strip()}")
