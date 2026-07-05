with open('4_diseno_sistema.tex', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
table_re = re.compile(r'\\begin\{table\}(.*?)\\end\{table\}', re.DOTALL)

for idx, m in enumerate(table_re.finditer(content)):
    print(f"\n--- Table {idx+1} ---")
    lines = m.group(0).split('\n')
    print('\n'.join(lines[:12]))
    print("...")
    print('\n'.join(lines[-6:]))
