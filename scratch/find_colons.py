import os
import re

tex_files = ['1_introduccion.tex', '2_contexto_estado_arte.tex', '3_analisis_requisitos.tex', 
             '4_diseno_sistema.tex', '5_seleccion_tecnologias.tex', '6_plan_implantacion.tex', 
             '7_evaluacion_sistema.tex', '8_presupuesto.tex', '9_planos_esquemas.tex', '10_conclusiones.tex']

for f_name in tex_files:
    with open(f_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match pattern: \item \textbf{...}: [CapitalizedWord]
    # Allow whitespace and commands
    pattern = r'\\item\s+\\textbf\{[^}]+\}:\s+([A-ZÁÉÍÓÚÑ][a-zA-Záéíóúñ]+)'
    for match in re.finditer(pattern, content):
        start = match.start()
        context = content[max(0, start-10):min(len(content), start + 120)].replace('\n', ' ')
        print(f"{f_name} -> Found '{match.group(1)}' after colon in context:")
        print(f"  {context}")
        print("-" * 50)
