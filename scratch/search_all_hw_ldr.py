import os

search_dir = "c:/Users/jacob/Downloads/TFG/Documento final"
search_term = "hw_ldr"

for filename in os.listdir(search_dir):
    if filename.endswith(".tex"):
        filepath = os.path.join(search_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            if search_term in line:
                print(f"Encontrado en {filename}:{idx+1}: {line.strip()}")
