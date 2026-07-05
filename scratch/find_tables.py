import os
import re

tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]
print("Tex files found:", tex_files)

# Regex to find table environments
table_re = re.compile(r'\\begin\{table\}(.*?)\\end\{table\}', re.DOTALL)

for fname in sorted(tex_files):
    if fname.startswith('__memoria_backup') or fname.startswith('ALMCACENAMIENTO'):
        continue
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    matches = list(table_re.finditer(content))
    if matches:
        print(f"\n=== File: {fname} (Found {len(matches)} tables) ===")
        for idx, match in enumerate(matches):
            table_body = match.group(1)
            # Find caption
            caption_match = re.search(r'\\caption\{(.*?)\}', table_body)
            caption_text = caption_match.group(1) if caption_match else "NO CAPTION"
            
            # Check position of caption relative to tabular
            tabular_pos = table_body.find(r'\begin{tabular')
            if tabular_pos == -1:
                tabular_pos = table_body.find(r'\begin{tabularx')
            caption_pos = table_body.find(r'\caption')
            
            pos_desc = "unknown"
            if tabular_pos != -1 and caption_pos != -1:
                pos_desc = "ABOVE" if caption_pos < tabular_pos else "BELOW"
                
            # Find table label
            label_match = re.search(r'\\label\{(.*?)\}', table_body)
            label_text = label_match.group(1) if label_match else "NO LABEL"
            
            # Check row coloring in table header (e.g. \rowcolor{...} or \cellcolor{...})
            has_rowcolor = "rowcolor" in table_body
            has_cellcolor = "cellcolor" in table_body
            
            print(f"Table {idx+1}: Label: {label_text} | Caption Pos: {pos_desc} | Header Coloring: rowcolor={has_rowcolor}, cellcolor={has_cellcolor}")
            print(f"   Caption: {caption_text[:100]}")
