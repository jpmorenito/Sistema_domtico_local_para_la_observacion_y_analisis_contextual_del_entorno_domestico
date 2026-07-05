import re
import os

tex_dir = r"c:\Users\jacob\Downloads\TFG\Documento final"

def extract_labels(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    tikz_blocks = re.findall(r'\\begin{tikzpicture}.*?\\end{tikzpicture}', content, re.DOTALL)
    for block_idx, block in enumerate(tikz_blocks):
        print(f"=== {filename} (Block {block_idx}) ===")
        # Look for text in braces inside the block
        # For example: node ... {Text};
        # We can find all instances of { ... } that are preceded by node or draw or similar
        # Or just look for nodes: \node ... { ... };
        # A simpler way is to find all \node statements
        nodes = re.findall(r'\\node\s*\[[^\]]*\]\s*\([^\)]*\)\s*(?:at\s*\([^\)]*\)\s*)?{([^}]*)};', block, re.DOTALL)
        for node in nodes:
            print(f"   Node: {node.strip().replace(chr(10), ' ')}")
            
        # Also let's print any text nodes or labels like: node[above] {Text}
        labels = re.findall(r'node\s*\[[^\]]*\]\s*{([^}]*)}', block, re.DOTALL)
        for label in labels:
            print(f"   Label: {label.strip().replace(chr(10), ' ')}")

for root, dirs, files in os.walk(tex_dir):
    for file in files:
        if file.endswith('.tex') and file not in ['__memoria.tex', '__memoria_temp.tex']:
            extract_labels(os.path.join(root, file))
