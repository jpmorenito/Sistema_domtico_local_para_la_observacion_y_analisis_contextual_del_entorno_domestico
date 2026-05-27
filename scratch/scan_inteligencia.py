import os
import re

tex_files = ['1_introduccion.tex', '2_contexto_estado_arte.tex', '3_analisis_requisitos.tex', 
             '4_diseno_sistema.tex', '5_seleccion_tecnologias.tex', '6_plan_implantacion.tex', 
             '7_evaluacion_sistema.tex', '8_presupuesto.tex', '9_planos_esquemas.tex', '10_conclusiones.tex']

for f_name in tex_files:
    with open(f_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all occurrences of Inteligencia or Artificial
    for match in re.finditer(r'\b(Inteligencia|Artificial)\b', content):
        start = match.start()
        context = content[max(0, start-40):min(len(content), start + 40)].replace('\n', ' ')
        print(f"{f_name} -> Found '{match.group(0)}' in context: ...{context}...")
