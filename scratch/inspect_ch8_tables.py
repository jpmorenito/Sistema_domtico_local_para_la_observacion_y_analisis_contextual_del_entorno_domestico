with open('8_presupuesto.tex', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
table_re = re.compile(r'\\begin\{table\}(.*?)\\end\{table\}', re.DOTALL)

for idx, m in enumerate(table_re.finditer(content)):
    print(f"\n--- Table {idx+1} ---")
    print(m.group(0))
