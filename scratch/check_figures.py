import re

with open("c:/Users/jacob/Downloads/TFG/Documento final/4_diseno_sistema.tex", "r", encoding="utf-8") as f:
    content = f.read()

# find all figure environments
figures = re.findall(r'\\begin{figure}.*?\\end{figure}', content, re.DOTALL)
print(f"Total figures: {len(figures)}")
for i, fig in enumerate(figures):
    print(f"\n--- Figure {i+1} ---")
    print("\n".join(fig.split("\n")[:15]))
