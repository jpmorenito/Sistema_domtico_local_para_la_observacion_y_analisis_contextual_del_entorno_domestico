import re
import difflib

# LaTeX file path
latex_file = "c:/Users/jacob/Downloads/TFG/Documento final/B_manual_tecnico_codigo.tex"

# Read LaTeX code blocks
with open(latex_file, "r", encoding="utf-8") as f:
    latex_content = f.read()

# Helper to extract code from lstlisting block
def get_latex_listing(label):
    pattern = r'\\begin\{lstlisting\}[^\]]*label=\{' + re.escape(label) + r'\}.*?\\end\{lstlisting\}'
    match = re.search(pattern, latex_content, re.DOTALL)
    if not match:
        return None
    block = match.group(0)
    # Extract only the content between \begin{lstlisting} and \end{lstlisting}
    content_match = re.search(r'\\begin\{lstlisting\}[^\]]*\}(.*?)\\end\{lstlisting\}', block, re.DOTALL)
    if content_match:
        return content_match.group(1).strip()
    return None

# Files to check
files_to_check = {
    "c:/Users/jacob/Downloads/TFG/pi_esp32-nodo-ambiente.yaml": "lst:code_nodo_ambiente",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-escritorio.yaml": "lst:code_nodo_escritorio",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-puerta.yaml": "lst:code_nodo_puerta",
    "c:/Users/jacob/Downloads/TFG/pi_automations.yaml": "lst:code_ha_automaciones"
}

for backup_path, label in files_to_check.items():
    print(f"\n==================================================")
    print(f"Comparing {backup_path} with LaTeX listing: {label}")
    print(f"==================================================")
    
    with open(backup_path, "r", encoding="utf-8") as f:
        pi_code = f.read().strip()
        
    latex_code = get_latex_listing(label)
    if not latex_code:
        print(f"Could not find listing with label {label} in LaTeX file.")
        continue
        
    # Clean up codes for comparison (normalize whitespace, line endings)
    pi_lines = [line.strip() for line in pi_code.splitlines() if line.strip()]
    latex_lines = [line.strip() for line in latex_code.splitlines() if line.strip()]
    
    # Compare
    if pi_lines == latex_lines:
        print("MATCH! The code in the document matches the backup file.")
    else:
        print("DIFFERENCE DETECTED!")
        # Print diff
        diff = difflib.unified_diff(
            latex_lines, 
            pi_lines, 
            fromfile='LaTeX Document', 
            tofile=f'Backup ({backup_path})', 
            lineterm=''
        )
        print("\n".join(list(diff)[:30])) # Show first 30 lines of diff
        if len(list(diff)) > 30:
            print("...")
