import os

for root, _, files in os.walk(r"C:\Users\jacob\Downloads\TFG\Documento final"):
    for file in files:
        if file.endswith(".tex"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        if "\\ne" in line:
                            print(f"{file} line {i+1}: {line.strip()}")
            except UnicodeDecodeError:
                pass
