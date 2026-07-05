import re
import os

tex_dir = r"c:\Users\jacob\Downloads\TFG\Documento final"

gerund_pattern = re.compile(r'\b\w+(ando|iendo|iéndose|ándose|ándolos|ándolas|iéndolos|iéndolas)\b', re.IGNORECASE)

anglicisms_list = [
    'customizar', 'customizado', 'customización', 'customise',
    'debuggear', 'debuggeado', 'debugging', 'debug',
    'deployar', 'deployado', 'deploy',
    'parsear', 'parseado', 'parser',
    'orquestar', 'orquestado', 'orquestación',
    'virtualizar', 'virtualizado', 'virtualización',
    'socket', 'sockets',
    'keepalive',
    'host', 'bridge',
    'peer-to-peer',
    'mmWave', 'FMCW'
]

anglicism_patterns = [(w, re.compile(rf'\b{w}\w*\b', re.IGNORECASE)) for w in anglicisms_list]

results = []

for root, dirs, files in os.walk(tex_dir):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            in_listing = False
            in_verbatim = False
            
            for idx, line in enumerate(lines):
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
                
                # Check gerunds
                gerunds = [m.group(0) for m in gerund_pattern.finditer(line)]
                # Check jargon
                jargons = []
                for w, pat in anglicism_patterns:
                    found = pat.findall(line)
                    if found:
                        jargons.extend(found)
                        
                if gerunds or jargons:
                    results.append({
                        'file': file,
                        'line': idx + 1,
                        'content': striped,
                        'gerunds': gerunds,
                        'jargons': jargons
                    })

print(f"Total entries found: {len(results)}")
# Print first 100 entries clearly
for idx, res in enumerate(results[:100]):
    print(f"{idx+1}. {res['file']}:{res['line']}:")
    print(f"   Text: \"{res['content']}\"")
    if res['gerunds']:
        print(f"   Gerunds: {res['gerunds']}")
    if res['jargons']:
        print(f"   Jargon/Anglicism: {res['jargons']}")
    print("-" * 40)
