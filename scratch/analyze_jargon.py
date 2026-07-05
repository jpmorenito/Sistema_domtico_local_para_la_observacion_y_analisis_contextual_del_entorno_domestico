import re
import os

tex_dir = r"c:\Users\jacob\Downloads\TFG\Documento final"

# Common gerund endings: ando, iendo
gerund_pattern = re.compile(r'\b\w+(ando|iendo|iéndose|ándose|ándolos|ándolas|iéndolos|iéndolas)\b', re.IGNORECASE)

# Technical jargon/Anglicisms
anglicisms_list = [
    'customizar', 'customizado', 'customización', 'customise',
    'debuggear', 'debuggeado', 'debugging', 'debug',
    'inicializar', 'inicializado', 'inicialización', 'initialize',
    'orquestar', 'orquestado', 'orquestación',
    'deployar', 'deployado', 'deploy',
    'virtualizar', 'virtualizado', 'virtualización',
    'contenedor', 'contenedores', 'container', 'containers',
    'desacoplar', 'desacoplado', 'desacoplamiento',
    'enrutar', 'enrutado', 'enrutamiento',
    'parsear', 'parseado', 'parser',
    'socket', 'sockets',
    'ping', 'pings',
    'keepalive',
    'host', 'bridge',
    'peer-to-peer',
    'mmWave', 'FMCW'
]

anglicism_patterns = [re.compile(rf'\b{w}\b', re.IGNORECASE) for w in anglicisms_list]

def analyze_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    in_listing = False
    in_verbatim = False
    
    for i, line in enumerate(lines):
        striped = line.strip()
        if '\\begin{lstlisting}' in striped or '\\begin{verbatim}' in striped:
            in_listing = True
            continue
        if '\\end{lstlisting}' in striped or '\\end{verbatim}' in striped:
            in_listing = False
            continue
        if in_listing or in_verbatim:
            continue
        if striped.startswith('%'):
            continue
            
        # 1. Look for ALL-CAPS words (length >= 4) that are not LaTeX commands, inside TikZ or normal text
        # (Exclude LaTeX commands starting with \)
        words = re.findall(r'\b[A-ZÁÉÍÓÚÑ]{4,}\b', line)
        for w in words:
            # Skip common abbreviations or LaTeX keywords like GPIO, ESP, RAM, CPU, SAI, LDR, DHT, IP, WAN, LAN, VPN, TCP, UART, Lovelace
            if w not in ['GPIO', 'ESP', 'RAM', 'CPU', 'SAI', 'LDR', 'DHT', 'IP', 'WAN', 'LAN', 'VPN', 'TCP', 'UART', 'Noise', 'HTML', 'YAML', 'JSON', 'REST', 'HTTP', 'HTTPS', 'WLAN', 'FMCW', 'Noise', 'noise', 'Noise', 'Noise', 'Noise', 'Noise', 'Noise', 'Noise', 'Noise', 'Noise']:
                print(f"[ALL-CAPS] {filename}:{i+1}: '{w}' in line: {line.strip()}")
                
        # 2. Look for gerunds
        gerunds = gerund_pattern.findall(line)
        if gerunds:
            # print the actual matching words
            matches = [m.group(0) for m in gerund_pattern.finditer(line)]
            print(f"[GERUND] {filename}:{i+1}: {matches} in line: {line.strip()}")
            
        # 3. Look for anglicisms / jargon
        for w_pat, w in zip(anglicism_patterns, anglicisms_list):
            if w_pat.search(line):
                print(f"[JARGON] {filename}:{i+1}: '{w}' in line: {line.strip()}")

print("Analyzing LaTeX files...")
for root, dirs, files in os.walk(tex_dir):
    for file in files:
        if file.endswith('.tex'):
            analyze_file(os.path.join(root, file))
