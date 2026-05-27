import os
import re

tex_files = ['1_introduccion.tex', '2_contexto_estado_arte.tex', '3_analisis_requisitos.tex', 
             '4_diseno_sistema.tex', '5_seleccion_tecnologias.tex', '6_plan_implantacion.tex', 
             '7_evaluacion_sistema.tex', '10_conclusiones.tex']

lowercase_words = {'Hardware', 'Software', 'Cliente', 'Servidor', 'Enrutador', 'Microcontrolador', 
                   'Sensor', 'Relé', 'Diodo', 'Láser', 'Banda', 'Frecuencia', 'Latencia', 
                   'Consumo', 'Energía', 'Coste', 'Presupuesto', 'Licencia'}

def analyze_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line_num, line in enumerate(lines, 1):
        line_strip = line.strip()
        # Ignore structural commands, comments, tables, figures
        if not line_strip or line_strip.startswith('%') or line_strip.startswith('\\') or line_strip.startswith('}') or line_strip.startswith(']'):
            continue
        if 'begin{' in line or 'end{' in line or '\\item' in line or '\\caption' in line:
            continue
            
        # Find capitalized words
        words = re.findall(r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\b', line)
        for word in words:
            if word not in lowercase_words:
                continue
                
            idx = line.find(word)
            preceding = line[:idx].strip()
            
            # Check context
            if preceding:
                last_char = preceding[-1]
                # If it's the start of a sentence
                if last_char in {'.', ':', '?', '!'}:
                    continue
                # If it follows a LaTeX command like \textbf{ or \texttt{
                if preceding.endswith('{') or preceding.endswith('~'):
                    # Check if the command preceding the brace is a section or something similar
                    # For example, in \textbf{Hardware} or \texttt{Hardware}
                    last_brace_open = preceding.rfind('{')
                    if last_brace_open != -1:
                        cmd = preceding[:last_brace_open].strip()
                        if cmd.endswith('\\section') or cmd.endswith('\\subsection') or cmd.endswith('\\subsubsection') or cmd.endswith('\\caption'):
                            continue
            else:
                # Start of line
                continue
                
            # If we get here, it's a potential error in running text
            print(f"{file_name}:{line_num} -> Word '{word}' in running text:")
            print(f"  Context: ...{line_strip[max(0, idx-40):min(len(line_strip), idx+40)]}...")
            print("-" * 50)

for f in tex_files:
    analyze_file(f)
