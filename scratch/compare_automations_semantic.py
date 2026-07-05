import re
import difflib

# Read LaTeX
latex_file = "c:/Users/jacob/Downloads/TFG/Documento final/B_manual_tecnico_codigo.tex"
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

# Read backup automations
with open("c:/Users/jacob/Downloads/TFG/pi_automations.yaml", "r", encoding="utf-8") as f:
    automations_content = f.read()

# Normalizer for YAML content for semantic comparison
def normalize_yaml_block(text):
    lines = []
    for line in text.splitlines():
        # Remove comments
        line = re.sub(r'#.*$', '', line)
        line = line.strip()
        if not line:
            continue
        
        # Normalize quotes
        line = line.replace("'", '"')
        
        # Normalize colons
        line = re.compile(r'\s*:\s*').sub(': ', line)
        
        # Clean accents
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N'
        }
        for k, v in replacements.items():
            line = line.replace(k, v)
            
        # Clean special emojis/characters if any
        line = re.sub(r'[^\x00-\x7F]+', '', line) # Keep only ASCII
        
        # If line contains id:, check if quotes are missing in backup vs latex and strip them
        if line.startswith("- id:"):
            # strip quotes
            line = "- id: " + line.split(":", 1)[1].strip().replace('"', '')
            
        lines.append(line)
    return lines

# Split backup automations by - id:
# Note: we need to parse them as individual blocks
blocks = re.split(r'\n-\s*id:', automations_content)
pi_automations = []
for idx, b in enumerate(blocks):
    b_full = "- id:" + b if idx > 0 or b.startswith("- id:") else b
    b_full = b_full.strip()
    if b_full:
        pi_automations.append(b_full)

# Find matching automation in backup
def find_matching_pi_automation(latex_lines):
    # Let's find by alias first
    # Extract alias from latex lines
    alias_line = None
    for line in latex_lines:
        if line.startswith("alias:"):
            alias_line = line
            break
    
    if alias_line:
        # Get alias value
        alias_val = alias_line.split(":", 1)[1].strip()
        # Find block containing alias
        for b in pi_automations:
            b_norm = normalize_yaml_block(b)
            for l in b_norm:
                if l.startswith("alias:") and alias_val in l:
                    return b
                    
    # If no alias found or no match, do a similarity match
    best_match = None
    best_ratio = 0
    latex_str = "\n".join(latex_lines)
    for b in pi_automations:
        b_norm_str = "\n".join(normalize_yaml_block(b))
        ratio = difflib.SequenceMatcher(None, latex_str, b_norm_str).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = b
            
    if best_ratio > 0.5:
        return best_match
    return None

automation_labels = [
    ("lst:auto_climatizacion", "Termostato Inteligente: Modo Estudio"),
    ("lst:auto_bienestar_resumen", "Analista Local: Resumen Diario de Bienestar"),
    ("lst:auto_detect_estudio", "Contexto: Detección de Estudio (Radar Espacial)"),
    ("lst:auto_detect_sueno", "Contexto: Detección de Sueño (Fusión Radar + LDR)"),
    ("lst:auto_seguridad_alarma", "Seguridad: Alarma por Radar (Modo Manual)"),
    ("lst:auto_procrastinacion_sueno", "Bienestar: Alerta Anti-Procrastinación de Sueño"),
    ("lst:auto_ergonomia_iluminacion", "Bienestar: Iluminación Ergonomía Activa"),
    ("lst:auto_pomodoro", "Bienestar: Break Dinámico (Pomodoro)"),
    ("lst:auto_ausencia", "Contexto: Ausencia Automática por Inactividad")
]

print("=== SEMANTIC COMPARISON OF HA AUTOMATIONS ===")
for label, name in automation_labels:
    print(f"\nChecking: {name} ({label})")
    latex_code = get_latex_listing(label)
    if not latex_code:
        print(f"Error: Could not find LaTeX listing for {label}")
        continue
        
    latex_norm = normalize_yaml_block(latex_code)
    matching_pi = find_matching_pi_automation(latex_norm)
    
    if not matching_pi:
        print("ERROR: No matching automation found in backup!")
        continue
        
    pi_norm = normalize_yaml_block(matching_pi)
    
    if latex_norm == pi_norm:
        print("SEMANTIC MATCH! (Logically identical.)")
    else:
        print("DIFFERENCE DETECTED!")
        diff = list(difflib.unified_diff(
            latex_norm,
            pi_norm,
            fromfile='LaTeX Document (Normalized)',
            tofile='Backup (Normalized)',
            lineterm=''
        ))
        print("\n".join(diff))
