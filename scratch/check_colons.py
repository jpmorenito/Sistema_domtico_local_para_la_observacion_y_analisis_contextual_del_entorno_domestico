import re
import os

tex_dir = r"c:\Users\jacob\Downloads\TFG\Documento final"

pattern = re.compile(r':\s+([A-ZÁÉÍÓÚa-z-zñáéíóúüñ])')

def analyze_file(filepath):
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
            
        # Ignore comments
        if striped.startswith('%'):
            continue
            
        # Search for colons followed by a space
        matches = re.finditer(r':\s+([A-ZÁÉÍÓÚ]\w*)', line)
        for m in matches:
            word = m.group(1)
            # Check if it's a proper noun/special keyword that should remain uppercase
            # E.g. Home Assistant, ESPHome, Docker, Raspberry, etc.
            # We will print all of them so we can decide
            print(f"{os.path.basename(filepath)}:{i+1}: {line.strip()} (Word after colon: {word})")

for root, dirs, files in os.walk(tex_dir):
    for file in files:
        if file.endswith('.tex'):
            analyze_file(os.path.join(root, file))
