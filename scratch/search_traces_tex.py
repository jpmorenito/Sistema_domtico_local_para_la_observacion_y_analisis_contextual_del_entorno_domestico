import os
import re

tfg_path = "c:/Users/jacob/Downloads/TFG/Documento final"
tex_files = [f for f in os.listdir(tfg_path) if f.endswith(".tex")]

print("Searching for trace images or commented figure blocks in LaTeX files:")
for file in tex_files:
    path = os.path.join(tfg_path, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find any figure environment containing traza or placeholders
    matches = re.finditer(r'\\begin\{figure\}.*?\\end\{figure\}', content, re.DOTALL)
    for m in matches:
        fig_block = m.group(0)
        if "traza" in fig_block.lower() or "fbox" in fig_block.lower() or "captura" in fig_block.lower():
            lines = fig_block.strip().split("\n")
            print(f"\n[{file}] Found relevant figure block:")
            print("-" * 50)
            for line in lines:
                print(line)
            print("-" * 50)
