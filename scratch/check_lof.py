with open("c:/Users/jacob/Downloads/TFG/Documento final/__memoria.lof", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    if "clases" in line or "16" in line or "17" in line:
        print(line.strip())
