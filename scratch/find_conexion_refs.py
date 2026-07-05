import glob
import re

tex_files = glob.glob("c:/Users/jacob/Downloads/TFG/Documento final/*.tex")
patterns = ["fig:conexion_ambiente", "fig:conexion_escritorio", "fig:conexion_puerta", "fig:conexion"]

for file_path in tex_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    for pattern in patterns:
        matches = list(re.finditer(re.escape(pattern), content))
        if matches:
            print(f"Found '{pattern}' in {file_path.split('/')[-1]} ({len(matches)} matches)")
            for match in matches:
                start = content.rfind("\n", 0, match.start()) + 1
                end = content.find("\n", match.end())
                print(f"  Line: {content[start:end].strip()}")
