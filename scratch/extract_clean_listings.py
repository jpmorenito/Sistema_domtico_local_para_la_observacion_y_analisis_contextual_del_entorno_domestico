import re

latex_file = "c:/Users/jacob/Downloads/TFG/Documento final/B_manual_tecnico_codigo.tex"
with open(latex_file, "r", encoding="utf-8") as f:
    content = f.read()

# Find all \begin{lstlisting}[...] and extract the label
matches = re.finditer(r'\\begin\{lstlisting\}\[(.*?)\]', content, re.DOTALL)
for i, m in enumerate(matches):
    opts = m.group(1)
    label_match = re.search(r'label=\{(.*?)\}', opts)
    lbl = label_match.group(1) if label_match else "No Label"
    print(f"Listing {i+1}: Label = {lbl}")
