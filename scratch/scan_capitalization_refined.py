import os
import re

tex_files = ['1_introduccion.tex', '2_contexto_estado_arte.tex', '3_analisis_requisitos.tex', 
             '4_diseno_sistema.tex', '5_seleccion_tecnologias.tex', '6_plan_implantacion.tex', 
             '7_evaluacion_sistema.tex', '8_presupuesto.tex', '9_planos_esquemas.tex', '10_conclusiones.tex']

lowercase_targets = {
    'Hardware', 'Software', 'Servidor', 'Cliente', 'Enrutador', 'Microcontrolador', 
    'Sensor', 'Relé', 'Diodo', 'Láser', 'Banda', 'Frecuencia', 'Latencia', 
    'Consumo', 'Energía', 'Coste', 'Presupuesto', 'Licencia', 'Router'
}

matches = []

for file_name in tex_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line_num, line in enumerate(lines, 1):
        line_strip = line.strip()
        # Skip comment lines
        if line_strip.startswith('%'):
            continue
            
        for target in lowercase_targets:
            # Match word as a whole word, capitalized
            pattern = r'\b' + re.escape(target) + r'\b'
            for match in re.finditer(pattern, line):
                start = match.start()
                
                # Check preceding character to see if it's the start of a sentence or a command
                preceding = line[:start].strip()
                
                # If start of line
                if not preceding:
                    continue
                    
                last_char = preceding[-1]
                # If it's the start of a sentence
                if last_char in {'.', ':', '?', '!'}:
                    continue
                # If it's part of a command name like \texttt{...} or \ref{...}
                if preceding.endswith('\\') or re.search(r'\\[a-zA-Z]+$', preceding):
                    continue
                if preceding.endswith('{'):
                    # Check if inside standard formatting macro like \texttt, \textbf, \textit, \label, \ref
                    last_brace = preceding.rfind('{')
                    cmd = preceding[:last_brace].strip()
                    if cmd.endswith('\\label') or cmd.endswith('\\ref') or cmd.endswith('\\cite') or cmd.endswith('\\texttt') or cmd.endswith('\\lstinline') or cmd.endswith('\\input') or cmd.endswith('\\include'):
                        continue
                if preceding.endswith('~') or preceding.endswith('\\item') or preceding.endswith('\\textbf'):
                    continue
                    
                matches.append({
                    'file': file_name,
                    'line_num': line_num,
                    'word': target,
                    'context': line_strip[max(0, start-40):min(len(line_strip), start + 45)].replace('\n', ' ')
                })

print(f"Total potential capitalization errors found: {len(matches)}")
for m in matches:
    print(f"File: {m['file']}, Line: {m['line_num']}")
    print(f"  Word: '{m['word']}'")
    print(f"  Context: ...{m['context']}...")
    print("-" * 50)
