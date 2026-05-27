with open('10_conclusiones.tex', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r':\s*([a-zA-ZáéíóúñÁÉÍÓÚÑ]+)', text)
print("Matches with simple regex:", matches)

pattern = r'\\item\s+\\textbf\{[^}]+\}:\s+([A-ZÁÉÍÓÚÑ][a-zA-Záéíóúñ]+)'
print("Full pattern search:")
for m in re.finditer(pattern, text):
    print("Match:", m.group(0))
