import re
import os

tex_dir = r"c:\Users\jacob\Downloads\TFG\Documento final"

# Find nodes or text inside tikzpicture
# We look for \begin{tikzpicture} to \end{tikzpicture}
# and inside them search for all-caps words (length >= 4) that are not LaTeX commands,
# or words after colons.

def analyze_tikz(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    tikz_blocks = re.findall(r'\\begin{tikzpicture}.*?\\end{tikzpicture}', content, re.DOTALL)
    
    for block_idx, block in enumerate(tikz_blocks):
        # Look for colons
        lines = block.split('\n')
        for i, line in enumerate(lines):
            # Ignore comments
            if line.strip().startswith('%'):
                continue
            # Search for colons followed by letter
            matches = re.finditer(r':\s+([A-Za-zÁÉÍÓÚáéíóúüñÑ])', line)
            for m in matches:
                char = m.group(1)
                print(f"[TIKZ-COLON] {filename} (block {block_idx}, line {i}): '{line.strip()}' (Char after colon: {char})")
                
            # Search for ALL-CAPS words (length >= 4)
            words = re.findall(r'\b[A-ZÁÉÍÓÚÑ]{4,}\b', line)
            for w in words:
                if w not in ['GPIO', 'ESP', 'RAM', 'CPU', 'SAI', 'LDR', 'DHT', 'IP', 'WAN', 'LAN', 'VPN', 'TCP', 'UART', 'Noise', 'Noise', 'Noise', 'Noise', 'Noise', 'Noise', 'Noise']:
                    print(f"[TIKZ-ALLCAPS] {filename} (block {block_idx}, line {i}): '{w}' in line: '{line.strip()}'")

print("Searching in TikZ blocks...")
for root, dirs, files in os.walk(tex_dir):
    for file in files:
        if file.endswith('.tex'):
            analyze_tikz(os.path.join(root, file))
