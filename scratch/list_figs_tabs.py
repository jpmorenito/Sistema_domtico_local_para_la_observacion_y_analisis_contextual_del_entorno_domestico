import os
import re

tex_files = [
    "1_introduccion.tex",
    "2_contexto_estado_arte.tex",
    "3_analisis_requisitos.tex",
    "4_diseno_sistema.tex",
    "5_seleccion_tecnologias.tex",
    "6_plan_implantacion.tex",
    "7_evaluacion_sistema.tex",
    "8_presupuesto.tex",
    "9_planos_esquemas.tex",
    "10_conclusiones.tex",
    "A_manual_usuario.tex",
    "B_manual_tecnico_codigo.tex"
]

base_dir = "c:/Users/jacob/Downloads/TFG/Documento final"

figures = []
tables = []

fig_pattern = re.compile(r'\\begin\{figure\}(.*?)\\end\{figure\}', re.DOTALL)
tab_pattern = re.compile(r'\\begin\{table\}(.*?)\\end\{table\}', re.DOTALL)
caption_pattern = re.compile(r'\\caption\{(.*?)\}')
label_pattern = re.compile(r'\\label\{(.*?)\}')

fig_count = 0
tab_count = 0

print("--- FIGURAS ENCONTRADAS ---")
for file_name in tex_files:
    path = os.path.join(base_dir, file_name)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Encontrar todas las figuras
        for match in fig_pattern.finditer(content):
            fig_count += 1
            fig_body = match.group(1)
            cap_m = caption_pattern.search(fig_body)
            lbl_m = label_pattern.search(fig_body)
            caption = cap_m.group(1) if cap_m else "SIN CAPTION"
            label = lbl_m.group(1) if lbl_m else "SIN LABEL"
            print(f"Figura {fig_count}: Label={label} | Caption={caption[:60]} | Archivo={file_name}")

print("\n--- TABLAS ENCONTRADAS ---")
for file_name in tex_files:
    path = os.path.join(base_dir, file_name)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Encontrar todas las tablas
        for match in tab_pattern.finditer(content):
            tab_count += 1
            tab_body = match.group(1)
            cap_m = caption_pattern.search(tab_body)
            lbl_m = label_pattern.search(tab_body)
            caption = cap_m.group(1) if cap_m else "SIN CAPTION"
            label = lbl_m.group(1) if lbl_m else "SIN LABEL"
            print(f"Tabla {tab_count}: Label={label} | Caption={caption[:60]} | Archivo={file_name}")
