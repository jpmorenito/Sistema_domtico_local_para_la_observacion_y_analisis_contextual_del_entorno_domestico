import os

for root, dirs, files in os.walk("c:/Users/jacob/Downloads/TFG/Documento final"):
    for file in files:
        if file.endswith(".yaml") or file.endswith(".yml"):
            path = os.path.join(root, file)
            print(f"Found: {os.path.relpath(path, 'c:/Users/jacob/Downloads/TFG/Documento final')} ({os.path.getsize(path)} bytes)")
