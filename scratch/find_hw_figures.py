with open("c:/Users/jacob/Downloads/TFG/Documento final/5_seleccion_tecnologias.tex", "r", encoding="utf-8") as f:
    content = f.read()

import re
figures = re.findall(r'\\begin{figure}.*?\\end{figure}', content, re.DOTALL)
for fig in figures:
    captions = re.findall(r'\\caption\{(.*?)\}', fig)
    labels = re.findall(r'\\label\{(.*?)\}', fig)
    print(f"Caption: {captions}, Label: {labels}")
