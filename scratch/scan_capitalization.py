import os
import re

tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]

# Words that are allowed to be capitalized (proper nouns, technologies, acronyms)
allowed_words = {
    'ESP32', 'Raspberry', 'Pi', 'Docker', 'Portainer', 'Home', 'Assistant', 'SQLite',
    'Tailscale', 'WireGuard', 'Wi-Fi', 'Ethernet', 'UART', 'GPIO', 'CPU', 'RAM', 'LDR',
    'DHT11', 'FMCW', 'ISM', 'Noise', 'YAML', 'TCP', 'IP', 'VPN', 'HTTP', 'HTTPS', 'IEEE',
    'Lovelace', 'Noise', 'SQLite', 'Portainer', 'Sonoff', 'Tuya', 'Smart', 'eWeLink', 'SmartLife',
    'JSON', 'XML', 'PC', 'OS', 'LED', 'ADC', 'DAC', 'GND', 'VIN', 'TX', 'RX', 'TX2', 'RX2', 'TTL',
    'HTML', 'CSS', 'WAN', 'WLAN', 'DNS', 'UCO', 'Córdoba', 'TFG', 'Trabajo', 'Fin', 'Grado',
    'Capítulo', 'Sección', 'Figura', 'Tabla', 'Código', 'Ecuación', 'Anexo', 'Apéndice',
    'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
    'Pomodoro', 'Babel', 'TikZ', 'LaTeX', 'TeX', 'PDF'
}

# Add common Spanish proper names or abbreviations that can be capitalized
allowed_words.update({
    'Cama', 'Escritorio', 'Silla', 'Puerta', 'Láser', 'Ambiente', 'Clima', 'Relé', 'SSR',
    'N1', 'N2', 'N3', 'A', 'B', 'C', 'D'
})

lowercase_suggestions = {
    'Hardware': 'hardware',
    'Software': 'software',
    'Internet': 'internet', # in Spanish, "internet" is increasingly lowercase
    'Cliente': 'cliente',
    'Servidor': 'servidor',
    'Inalámbrica': 'inalámbrica',
    'Láser': 'láser',
    'Temperatura': 'temperatura',
    'Humedad': 'humedad',
    'Luminosidad': 'luminosidad',
    'Acústico': 'acústico',
    'Presencia': 'presencia',
    'Ocupación': 'ocupación',
    'Seguridad': 'seguridad',
    'Acceso': 'acceso',
    'Conexión': 'conexión',
    'Comunicaciones': 'comunicaciones',
    'Enrutador': 'enrutador',
    'Red': 'red',
    'Microcontrolador': 'microcontrolador',
    'Sensor': 'sensor',
    'Relé': 'relé',
    'Diodo': 'diodo',
    'Banda': 'banda',
    'Frecuencia': 'frecuencia',
    'Latencia': 'latencia',
    'Consumo': 'consumo',
    'Energía': 'energía',
    'Coste': 'coste',
    'Presupuesto': 'presupuesto',
    'Licencia': 'licencia',
    'Mano': 'mano',
    'Obra': 'obra',
    'Enero': 'enero', 'Febrero': 'febrero', 'Marzo': 'marzo', 'Abril': 'abril',
    'Mayo': 'mayo', 'Junio': 'junio', 'Julio': 'julio', 'Agosto': 'agosto',
    'Septiembre': 'septiembre', 'Octubre': 'octubre', 'Noviembre': 'noviembre',
    'Diciembre': 'diciembre',
    'Lunes': 'lunes', 'Martes': 'martes', 'Miércoles': 'miércoles', 'Jueves': 'jueves',
    'Viernes': 'viernes', 'Sábado': 'sábado', 'Domingo': 'domingo',
    'Español': 'español', 'Inglés': 'inglés', 'Francés': 'francés', 'Alemán': 'alemán'
}

for file_name in sorted(tex_files):
    if file_name.startswith('__memoria_temp') or file_name == 'ALMCACENAMIENTO_TEMPORAL.tex':
        continue
    print(f"\nScanning {file_name}...")
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line_num, line in enumerate(lines, 1):
        # Ignore comments and tikzpicture environments for simple scanner
        if line.strip().startswith('%') or 'tikzpicture' in line or 'node[' in line or '\\draw' in line:
            continue
            
        # Find all capitalized words
        words = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b', line)
        for word in words:
            if word in allowed_words:
                continue
                
            # Check if it starts a sentence or is after punctuation
            # A word is at the start if it is the first word in a line (ignoring LaTeX macros) or follows a period/colon
            # Let's check the context of the word in the line
            idx = line.find(word)
            if idx > 0:
                preceding = line[:idx].strip()
                # If it follows a period, colon, question mark, or is inside a macro like \section{...}
                if preceding and (preceding[-1] in {'.', ':', '?', '!'} or preceding.endswith('\\item') or preceding.endswith('\\textbf')):
                    continue
                # If it is part of a title macro like \section{Word...}
                if '\\section' in preceding or '\\subsection' in preceding or '\\subsubsection' in preceding or '\\caption' in preceding or '\\paragraph' in preceding:
                    # Capitalization in section titles is usually okay or handled separately
                    continue
                    
            if idx == 0:
                # First word of the line, usually okay
                continue
                
            # Print potential issue
            if word in lowercase_suggestions:
                print(f"  Line {line_num}: Potential capitalization error '{word}' -> '{lowercase_suggestions[word]}'")
                print(f"    Line content: {line.strip()[:100]}")
            else:
                # Print other capitalized words that are not in allowed list
                # (to see if they are proper nouns or errors)
                print(f"  Line {line_num}: Capitalized word '{word}' (not in allowed list)")
                print(f"    Line content: {line.strip()[:100]}")
