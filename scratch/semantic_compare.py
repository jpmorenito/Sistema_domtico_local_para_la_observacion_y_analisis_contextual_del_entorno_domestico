import re
import difflib

def clean_code(text):
    cleaned_lines = []
    for line in text.splitlines():
        # Remove comments
        line_no_comment = re.sub(r'#.*$', '', line).strip()
        if not line_no_comment:
            continue
        # Normalize quotes (replace ' with ")
        line_norm_quotes = line_no_comment.replace("'", '"')
        # Normalize spaces around colons
        line_norm_spaces = re.sub(r'\s*:\s*', ': ', line_norm_quotes).strip()
        # Clean accents for comparison
        line_clean = line_norm_spaces
        replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n',
                        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N'}
        for k, v in replacements.items():
            line_clean = line_clean.replace(k, v)
        cleaned_lines.append(line_clean)
    return cleaned_lines

# Read LaTeX
latex_file = "c:/Users/jacob/Downloads/TFG/Documento final/B_manual_tecnico_codigo.tex"
with open(latex_file, "r", encoding="utf-8") as f:
    latex_content = f.read()

def get_latex_listing(label):
    matches = re.finditer(r'\\begin\{lstlisting\}[^\]]*\}(.*?)\\end\{lstlisting\}', latex_content, re.DOTALL)
    for m in matches:
        full_match = m.group(0)
        if label in full_match:
            return m.group(1).strip()
    return None

files_to_check = {
    "c:/Users/jacob/Downloads/TFG/pi_esp32-nodo-ambiente.yaml": "lst:code_nodo_ambiente",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-escritorio.yaml": "lst:code_nodo_escritorio",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-puerta.yaml": "lst:code_nodo_puerta"
}

print("=== SEMANTIC COMPARISON OF NODES ===")
for backup_path, label in files_to_check.items():
    print(f"\nComparing {backup_path.split('/')[-1]} with LaTeX: {label}")
    with open(backup_path, "r", encoding="utf-8") as f:
        pi_code = f.read().strip()
        
    latex_code = get_latex_listing(label)
    if not latex_code:
        print(f"Error: Could not find LaTeX listing for {label}")
        continue
        
    pi_clean = clean_code(pi_code)
    latex_clean = clean_code(latex_code)
    
    if pi_clean == latex_clean:
        print("SEMANTIC MATCH! (Functionally identical, differences are only comments, quotes, or accents.)")
    else:
        print("SEMANTIC DIFFERENCE FOUND!")
        diff = list(difflib.unified_diff(
            latex_clean,
            pi_clean,
            fromfile='LaTeX Document (Cleaned)',
            tofile='Backup (Cleaned)',
            lineterm=''
        ))
        print("\n".join(diff))
