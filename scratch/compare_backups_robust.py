import re
import difflib

# LaTeX file path
latex_file = "c:/Users/jacob/Downloads/TFG/Documento final/B_manual_tecnico_codigo.tex"

# Read LaTeX content
with open(latex_file, "r", encoding="utf-8") as f:
    latex_content = f.read()

# Helper to extract code from lstlisting block
def get_latex_listing(label):
    matches = re.finditer(r'\\begin\{lstlisting\}(?:\[.*?\])?(.*?)\\end\{lstlisting\}', latex_content, re.DOTALL)
    for m in matches:
        full_match = m.group(0)
        if label in full_match:
            return m.group(1).strip()
    return None

# Files to check
nodes_to_check = {
    "c:/Users/jacob/Downloads/TFG/pi_esp32-nodo-ambiente.yaml": "lst:code_nodo_ambiente",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-escritorio.yaml": "lst:code_nodo_escritorio",
    "c:/Users/jacob/Downloads/TFG/pi_esp32-zona-puerta.yaml": "lst:code_nodo_puerta"
}

print("=== COMPARING NODE CONFIGURATIONS ===")
for backup_path, label in nodes_to_check.items():
    print(f"\nComparing {backup_path.split('/')[-1]} with LaTeX: {label}")
    with open(backup_path, "r", encoding="utf-8") as f:
        pi_code = f.read().strip()
        
    latex_code = get_latex_listing(label)
    if not latex_code:
        print(f"Error: Could not find LaTeX listing for {label}")
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
        diff = list(difflib.unified_diff(
            latex_lines, 
            pi_lines, 
            fromfile='LaTeX Document', 
            tofile=f'Backup ({backup_path.split("/")[-1]})', 
            lineterm=''
        ))
        print("\n".join(diff[:15]))
        if len(diff) > 15:
            print("...")

print("\n=== COMPARING HA AUTOMATIONS ===")
# Read the complete automations.yaml backup
with open("c:/Users/jacob/Downloads/TFG/pi_automations.yaml", "r", encoding="utf-8") as f:
    automations_content = f.read()

# Let's clean the automations content for subsegment searching
# Home Assistant automations are blocks starting with '- id:'
# Let's extract the clean lines of the backup automations
backup_lines_all = [line.strip() for line in automations_content.splitlines() if line.strip()]

automation_labels = [
    "lst:auto_climatizacion",
    "lst:auto_bienestar_resumen",
    "lst:auto_detect_estudio",
    "lst:auto_detect_sueno",
    "lst:auto_seguridad_alarma",
    "lst:auto_procrastinacion_sueno",
    "lst:auto_ergonomia_iluminacion",
    "lst:auto_pomodoro",
    "lst:auto_ausencia"
]

for label in automation_labels:
    latex_code = get_latex_listing(label)
    if not latex_code:
        print(f"Error: Could not find LaTeX listing for {label}")
        continue
        
    print(f"\nChecking automation: {label}")
    latex_lines = [line.strip() for line in latex_code.splitlines() if line.strip()]
    
    # Let's search if the sequence of lines exists in the backup automations.yaml
    # Since the order of lines in YAML should be identical, let's find if all lines exist together.
    # We can do a substring search or a line-by-line block matching.
    # Since the files are clean, let's try to match the block.
    # We look for a sub-list of backup_lines_all that matches latex_lines.
    found = False
    for i in range(len(backup_lines_all) - len(latex_lines) + 1):
        sub_list = backup_lines_all[i:i+len(latex_lines)]
        if sub_list == latex_lines:
            found = True
            break
            
    if found:
        print("MATCH! The automation code in the document exists exactly as is in the backup.")
    else:
        print("DIFFERENCE DETECTED or NOT FOUND IN BACKUP!")
        # Let's try to find an automation block with the same alias in the backup and show a diff
        # Look for the alias in LaTeX listing
        alias_match = re.search(r"alias:\s*['\"]?(.*?)['\"]?\n", latex_code)
        if alias_match:
            alias = alias_match.group(1).strip()
            print(f"Searching by alias: '{alias}'")
            # Let's find the automation block in backup that contains this alias
            # Automations start with '- id:'
            blocks = re.split(r'\n-\s*id:', automations_content)
            matching_block = None
            for b in blocks:
                # Add '- id:' back since it was split
                b_full = "- id:" + b if not b.startswith("- id:") else b
                if alias in b_full:
                    matching_block = b_full
                    break
            
            if matching_block:
                pi_block_lines = [line.strip() for line in matching_block.splitlines() if line.strip()]
                diff = list(difflib.unified_diff(
                    latex_lines, 
                    pi_block_lines, 
                    fromfile='LaTeX Document', 
                    tofile='Backup (matching block)', 
                    lineterm=''
                ))
                print("\n".join(diff[:15]))
                if len(diff) > 15:
                    print("...")
            else:
                print(f"No automation with alias '{alias}' found in the backup file.")
        else:
            print("Could not extract alias from LaTeX listing to search in backup.")
