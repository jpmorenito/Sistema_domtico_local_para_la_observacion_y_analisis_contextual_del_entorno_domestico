# Let's inspect the LaTeX content of the tables to see how they are implemented.

with open('3_analisis_requisitos.tex', 'r', encoding='utf-8', errors='ignore') as f:
    ch3_content = f.read()

import re
table_re = re.compile(r'\\begin\{table\}(.*?)\\end\{table\}', re.DOTALL)

print("--- TABLE IN CHAPTER 3 ---")
m = table_re.search(ch3_content)
if m:
    print(m.group(0))

with open('7_evaluacion_sistema.tex', 'r', encoding='utf-8', errors='ignore') as f:
    ch7_content = f.read()

print("--- TABLE IN CHAPTER 7 ---")
m = table_re.search(ch7_content)
if m:
    print(m.group(0))

with open('8_presupuesto.tex', 'r', encoding='utf-8', errors='ignore') as f:
    ch8_content = f.read()

print("--- TABLE IN CHAPTER 8 ---")
m = table_re.search(ch8_content)
if m:
    print(m.group(0))
