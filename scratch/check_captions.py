import re

with open("c:/Users/jacob/Downloads/TFG/Documento final/4_diseno_sistema.tex", "r", encoding="utf-8") as f:
    content = f.read()

# find all figure environments
figures = re.findall(r'\\begin{figure}.*?\\end{figure}', content, re.DOTALL)
for i, fig in enumerate(figures[:7]):
    captions = re.findall(r'\\caption\{(.*?)\}', fig)
    labels = re.findall(r'\\label\{(.*?)\}', fig)
    print(f"Figure {i+1}:")
    print(f"  Captions: {captions}")
    print(f"  Labels: {labels}")
