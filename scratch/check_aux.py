with open("c:/Users/jacob/Downloads/TFG/Documento final/__memoria.aux", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    if "diagrama_clases" in line:
        print(line.strip())
