import glob
import re

tex_files = glob.glob("c:/Users/jacob/Downloads/TFG/Documento final/*.tex")
image_patterns = [
    "nodo_ambiente", "nodo_escritorio", "nodo_puerta",
    "conexion_nodo_ambiente", "conexion_nodo_escritorio", "conexion_nodo_puerta",
    "conexion_nodo"
]

for file_path in tex_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    for pattern in image_patterns:
        matches = list(re.finditer(re.escape(pattern), content, re.IGNORECASE))
        if matches:
            print(f"Found '{pattern}' in {file_path.split('/')[-1]} ({len(matches)} matches)")
            # Print matching lines
            for match in matches:
                # Find the line containing the match
                start = content.rfind("\n", 0, match.start()) + 1
                end = content.find("\n", match.end())
                print(f"  Line: {content[start:end].strip()}")
