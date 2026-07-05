import re

# 1. Fix Chapter 3 Table (3_analisis_requisitos.tex)
print("Fixing 3_analisis_requisitos.tex...")
with open('3_analisis_requisitos.tex', 'r', encoding='utf-8') as f:
    ch3 = f.read()

# Pattern to match:
# \begin{table}[H]
#     \centering
#     \caption{...}
#     \label{...}
#     \begin{tabular}{...}
#         ...
#     \end{tabular}
# \end{table}

ch3_table_pattern = re.compile(
    r'(\\begin\{table\}\[H\]\s*\\centering\s*)(\\caption\{.*?\})\s*(\\label\{.*?\})\s*(\\begin\{tabular\}.*?\\end\{tabular\})(\s*\\end\{table\})',
    re.DOTALL
)

def ch3_repl(match):
    prefix = match.group(1)
    caption = match.group(2)
    label = match.group(3)
    tabular = match.group(4)
    suffix = match.group(5)
    return f"{prefix}{tabular}\n    {caption}\n    {label}\n{suffix}"

ch3_fixed = ch3_table_pattern.sub(ch3_repl, ch3)

with open('3_analisis_requisitos.tex', 'w', encoding='utf-8') as f:
    f.write(ch3_fixed)


# 2. Fix Chapter 4 Tables (4_diseno_sistema.tex)
print("Fixing 4_diseno_sistema.tex...")
with open('4_diseno_sistema.tex', 'r', encoding='utf-8') as f:
    ch4 = f.read()

# Pattern to match tables with caption ABOVE:
# \begin{table}[H]
#     \centering
#     \caption{...}
#     \label{...}
#     \makebox[\textwidth][c]{
#     \begin{tabular}{...}
#         ...
#     \end{tabular}
#     }
# \end{table}

ch4_table_pattern = re.compile(
    r'(\\begin\{table\}\[H\]\s*\\centering\s*)(\\caption\{.*?\})\s*(\\label\{.*?\})\s*(\\makebox\[\\textwidth\]\[c\]\{\s*\\begin\{tabular\}.*?\\end\{tabular\}\s*\})(\s*\\end\{table\})',
    re.DOTALL
)

def ch4_repl(match):
    prefix = match.group(1)
    caption = match.group(2)
    label = match.group(3)
    makebox = match.group(4)
    suffix = match.group(5)
    return f"{prefix}{makebox}\n    {caption}\n    {label}\n{suffix}"

ch4_fixed = ch4_table_pattern.sub(ch4_repl, ch4)

with open('4_diseno_sistema.tex', 'w', encoding='utf-8') as f:
    f.write(ch4_fixed)


# 3. Fix Chapter 7 Table (7_evaluacion_sistema.tex)
print("Fixing 7_evaluacion_sistema.tex...")
with open('7_evaluacion_sistema.tex', 'r', encoding='utf-8') as f:
    ch7 = f.read()

# We need to insert \rowcolor[gray]{0.9} in the table.
# \begin{tabular}{|l|c|c|c|l|}
#     \hline
#     \multicolumn{1}{|c|}{\textbf{Componente}} & ...

ch7_target = r'''    \begin{tabular}{|l|c|c|c|l|}
        \hline
        \multicolumn{1}{|c|}{\textbf{Componente}}'''

ch7_replacement = r'''    \begin{tabular}{|l|c|c|c|l|}
        \hline
        \rowcolor[gray]{0.9} 
        \multicolumn{1}{|c|}{\textbf{Componente}}'''

if ch7_target in ch7:
    ch7_fixed = ch7.replace(ch7_target, ch7_replacement)
else:
    # Try with normal spacing
    ch7_target_alt = r'\begin{tabular}{|l|c|c|c|l|}' + '\n' + r'        \hline' + '\n' + r'        \multicolumn{1}{|c|}{\textbf{Componente}}'
    ch7_replacement_alt = r'\begin{tabular}{|l|c|c|c|l|}' + '\n' + r'        \hline' + '\n' + r'        \rowcolor[gray]{0.9}' + '\n' + r'        \multicolumn{1}{|c|}{\textbf{Componente}}'
    ch7_fixed = ch7.replace(ch7_target_alt, ch7_replacement_alt)

with open('7_evaluacion_sistema.tex', 'w', encoding='utf-8') as f:
    f.write(ch7_fixed)


# 4. Fix Chapter 8 Tables (8_presupuesto.tex)
print("Fixing 8_presupuesto.tex...")
with open('8_presupuesto.tex', 'r', encoding='utf-8') as f:
    ch8 = f.read()

# Table 1:
# \begin{tabular}{|l|c|c|r|r|}
#     \hline
#     \parbox[c]{4.2cm}{\vspace{0.15cm}\centering\textbf{Descripci

ch8_t1_target = r'''    \begin{tabular}{|l|c|c|r|r|}
        \hline
        \parbox[c]{4.2cm}{\vspace{0.15cm}\centering\textbf{Descripci'''

ch8_t1_replacement = r'''    \begin{tabular}{|l|c|c|r|r|}
        \hline
        \rowcolor[gray]{0.9} 
        \parbox[c]{4.2cm}{\vspace{0.15cm}\centering\textbf{Descripci'''

# Table 2:
# \begin{tabular}{|l|c|c|c|}
#     \hline
#     \parbox[c]{3.2cm}{\vspace{0.15cm}\centering\textbf{Software /\\Plataforma}\vspace{0.15cm}}

ch8_t2_target = r'''    \begin{tabular}{|l|c|c|c|}
        \hline
        \parbox[c]{3.2cm}{\vspace{0.15cm}\centering\textbf{Software /\\Plataforma}\vspace{0.15cm}}'''

ch8_t2_replacement = r'''    \begin{tabular}{|l|c|c|c|}
        \hline
        \rowcolor[gray]{0.9} 
        \parbox[c]{3.2cm}{\vspace{0.15cm}\centering\textbf{Software /\\Plataforma}\vspace{0.15cm}}'''

# Table 3:
# \begin{tabular}{|l|c|c|r|}
#     \hline
#     \parbox[c]{4.6cm}{\vspace{0.3cm}\centering\textbf{Fase de ingenier

ch8_t3_target = r'''    \begin{tabular}{|l|c|c|r|}
        \hline
        \parbox[c]{4.6cm}{\vspace{0.3cm}\centering\textbf{Fase de ingenier'''

ch8_t3_replacement = r'''    \begin{tabular}{|l|c|c|r|}
        \hline
        \rowcolor[gray]{0.9} 
        \parbox[c]{4.6cm}{\vspace{0.3cm}\centering\textbf{Fase de ingenier'''

# Table 4:
# \begin{tabular}{|l|r|}
#     \hline
#     \parbox[c]{9.5cm}{\vspace{0.15cm}\textbf{Concepto Presupuestario}\vspace{0.15cm}}

ch8_t4_target = r'''    \begin{tabular}{|l|r|}
        \hline
        \parbox[c]{9.5cm}{\vspace{0.15cm}\textbf{Concepto Presupuestario}\vspace{0.15cm}}'''

ch8_t4_replacement = r'''    \begin{tabular}{|l|r|}
        \hline
        \rowcolor[gray]{0.9} 
        \parbox[c]{9.5cm}{\vspace{0.15cm}\textbf{Concepto Presupuestario}\vspace{0.15cm}}'''

ch8_fixed = ch8
for t, r in [(ch8_t1_target, ch8_t1_replacement), 
             (ch8_t2_target, ch8_t2_replacement), 
             (ch8_t3_target, ch8_t3_replacement), 
             (ch8_t4_target, ch8_t4_replacement)]:
    if t in ch8_fixed:
        ch8_fixed = ch8_fixed.replace(t, r)
        print(f"Substituted target {t[:40]}...")
    else:
        print(f"Warning: target {t[:40]}... not found!")

with open('8_presupuesto.tex', 'w', encoding='utf-8') as f:
    f.write(ch8_fixed)

print("Done fixing tables!")
