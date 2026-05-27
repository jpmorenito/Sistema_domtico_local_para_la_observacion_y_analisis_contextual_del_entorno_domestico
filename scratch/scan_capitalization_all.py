import os
import re

tex_files = ['1_introduccion.tex', '2_contexto_estado_arte.tex', '3_analisis_requisitos.tex', 
             '4_diseno_sistema.tex', '5_seleccion_tecnologias.tex', '6_plan_implantacion.tex', 
             '7_evaluacion_sistema.tex', '8_presupuesto.tex', '9_planos_esquemas.tex', '10_conclusiones.tex']

allowed_acronyms = {
    'ESP32', 'SoC', 'Docker', 'Portainer', 'Home', 'Assistant', 'SQLite', 'Tailscale', 'WireGuard',
    'Wi-Fi', 'Ethernet', 'UART', 'GPIO', 'CPU', 'RAM', 'LDR', 'DHT11', 'FMCW', 'ISM', 'Noise',
    'YAML', 'TCP', 'IP', 'VPN', 'HTTP', 'HTTPS', 'IEEE', 'Lovelace', 'Sonoff', 'Tuya', 'Smart',
    'eWeLink', 'SmartLife', 'JSON', 'XML', 'PC', 'OS', 'LED', 'ADC', 'DAC', 'GND', 'VIN', 'TX',
    'RX', 'TX2', 'RX2', 'TTL', 'HTML', 'CSS', 'WAN', 'WLAN', 'DNS', 'UCO', 'TFG', 'FSM', 'PIR',
    'SSD', 'NAS', 'TinyML', 'TensorFlow', 'Lite', 'Whisper', 'Piper', 'Babel', 'TikZ', 'LaTeX', 'TeX', 'PDF',
    'Córdoba', 'UCO', 'Universidad', 'Granada', 'España', 'Europa', 'Jacob', 'Pino', 'Moreno',
    'José', 'Manuel', 'Palomares', 'Muñoz', 'Fernando', 'León', 'García'
}

ignored_patterns = [
    r'\\section', r'\\subsection', r'\\subsubsection', r'\\caption', r'\\label', r'\\ref', r'\\cite',
    r'\\texttt', r'\\lstinline', r'\\includegraphics', r'\\input', r'\\include', r'\\begin', r'\\end',
    r'\\fancyhead', r'\\fancyfoot', r'\\newcommand', r'\\renewcommand', r'\\usepackage', r'\\documentclass'
]

def is_capitalized_candidate(word):
    if word in allowed_acronyms:
        return False
    if word.isupper():
        return False
    return True

for f_name in tex_files:
    print(f"\nScanning {f_name}...")
    with open(f_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line_num, line in enumerate(lines, 1):
        line_strip = line.strip()
        if not line_strip or line_strip.startswith('%'):
            continue
            
        # Ignore lines with block commands
        if any(cmd in line_strip for cmd in ['\\begin{tikzpicture}', '\\draw', '\\node', '\\path', '\\fill']):
            continue
            
        # Find all words starting with capital letter
        words = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-zA-Záéíóúñ]+\b', line)
        for word in words:
            if not is_capitalized_candidate(word):
                continue
                
            idx = line.find(word)
            preceding = line[:idx].strip()
            
            # Check context
            if preceding:
                last_char = preceding[-1]
                # End of sentence
                if last_char in {'.', ':', '?', '!'}:
                    continue
                # Math mode or block
                if preceding.endswith('$') or preceding.endswith('~') or preceding.endswith('\\item'):
                    continue
                # Preceding LaTeX command
                if preceding.endswith('\\') or re.search(r'\\[a-zA-Z]+$', preceding):
                    continue
                if preceding.endswith('{'):
                    last_brace = preceding.rfind('{')
                    cmd = preceding[:last_brace].strip()
                    if any(cmd.endswith(pat) for pat in ignored_patterns):
                        continue
                        
            else:
                # Start of line
                continue
                
            # Print context
            print(f"  Line {line_num}: Word '{word}'")
            print(f"    Context: ...{line_strip[max(0, idx-30):min(len(line_strip), idx+45)]}...")
