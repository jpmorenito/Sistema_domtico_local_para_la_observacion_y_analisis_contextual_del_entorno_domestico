import os
import re

patterns = [r'192\.168\.\d+\.\d+', r'10\.\d+\.\d+\.\d+']

for root, dirs, files in os.walk("c:/Users/jacob/Downloads/TFG/Documento final"):
    if "scratch" in root or root == "c:/Users/jacob/Downloads/TFG/Documento final":
        for file in files:
            if file.endswith(".py") or file.endswith(".tex") or file.endswith(".txt") or file.endswith(".yaml"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            print(f"Found in {file}: {matches}")
                except Exception:
                    pass
