with open("c:/Users/jacob/Downloads/TFG/Documento final/5_seleccion_tecnologias.tex", "r", encoding="utf-8") as f:
    content = f.read()

import re
sections = re.findall(r'\\(?:section|subsection|subsubsection)\{.*?\}', content)
for sec in sections:
    print(sec)
