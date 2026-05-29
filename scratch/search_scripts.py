import os

project_dir = r"c:\Users\jacob\Downloads\TFG\Documento final"
print("Searching for python files in project...")

for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            print(f"Found python file: {path}")
            # Let's check if it contains conexion_nodo_escritorio or edit logic
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "conexion_nodo_escritorio.png" in content or "conexion_nodo_ambiente.png" in content:
                        print(f"  -> REFERENCES IMAGES!")
            except Exception as e:
                print(f"  -> Error reading: {e}")
