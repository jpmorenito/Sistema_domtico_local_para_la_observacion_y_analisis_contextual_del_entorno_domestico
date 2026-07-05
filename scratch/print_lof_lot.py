import os

lof_path = "c:/Users/jacob/Downloads/TFG/Documento final/__memoria.lof"
if os.path.exists(lof_path):
    with open(lof_path, "r", encoding="utf-8") as f:
        lof_content = f.read()
    print("=== FIGURES IN LIST OF FIGURES ===")
    for line in lof_content.split("\n"):
        if "contentsline {figure}" in line:
            print(line.strip())
else:
    print(f"{lof_path} not found")
