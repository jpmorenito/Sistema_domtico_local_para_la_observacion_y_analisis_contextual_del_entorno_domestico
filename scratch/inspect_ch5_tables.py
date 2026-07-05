# Let's inspect the tables in 5_seleccion_tecnologias.tex to check their rowcolor specification.

with open('5_seleccion_tecnologias.tex', 'r', encoding='utf-8', errors='ignore') as f:
    ch5_content = f.read()

import re
table_re = re.compile(r'\\begin\{table\}(.*?)\\end\{table\}', re.DOTALL)

for idx, m in enumerate(table_re.finditer(ch5_content)):
    print(f"--- Table {idx+1} ---")
    lines = m.group(0).split('\n')
    for line in lines:
        if 'rowcolor' in line or 'caption' in line:
            print(line.strip())
