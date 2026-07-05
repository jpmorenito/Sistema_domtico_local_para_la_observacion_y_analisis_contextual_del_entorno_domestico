import sys
import paramiko
import re
import difflib

# Reconfigure stdout to support UTF-8 characters (like emojis) in the Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

# LaTeX file path
latex_file = "c:/Users/jacob/Downloads/TFG/Documento final/B_manual_tecnico_codigo.tex"

with open(latex_file, "r", encoding="utf-8") as f:
    latex_content = f.read()

def get_latex_listing(label):
    pattern = r'\\begin\{lstlisting\}[^\]]*label=\{' + re.escape(label) + r'\}.*?\\end\{lstlisting\}'
    match = re.search(pattern, latex_content, re.DOTALL)
    if not match:
        return None
    block = match.group(0)
    content_match = re.search(r'\\begin\{lstlisting\}[^\]]*\}(.*?)\\end\{lstlisting\}', block, re.DOTALL)
    if content_match:
        text = content_match.group(1).strip()
        if text.startswith(']'):
            text = text[1:].strip()
        return text
    return None

# Text normalizer for matching aliases (removes case, accents, spaces, quotes)
def normalize_alias(alias):
    alias = alias.lower()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N',
        'ü': 'u', 'í': 'i'
    }
    for k, v in replacements.items():
        alias = alias.replace(k, v)
    alias = re.sub(r"[^a-z0-9]", "", alias)
    return alias

# Clean yaml lines for robust line-by-line comparison
def clean_yaml_line(line):
    line = re.sub(r'#.*$', '', line) # remove comments
    line = line.strip()
    line = line.replace("'", '"') # normalize quotes
    line = re.compile(r'\s*:\s*').sub(': ', line) # normalize colon spacing
    
    # replace accents
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ñ': 'N',
        'ü': 'u', 'í': 'i'
    }
    for k, v in replacements.items():
        line = line.replace(k, v)
    return line

def get_clean_lines(code_str):
    lines = []
    for line in code_str.splitlines():
        line_clean = clean_yaml_line(line)
        if line_clean and not line_clean.startswith("id:"):  # ignore automation IDs
            lines.append(line_clean)
    return lines

# Connect to Pi
hosts = ["100.70.173.44", "192.168.1.100", "jacob-pi"]
username = "jpmorenito"
password = "jpmorenito"

connected = False
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for host in hosts:
    try:
        print(f"Connecting to {host}...")
        ssh.connect(host, username=username, password=password, timeout=3)
        print(f"Connected to {host}!")
        connected = True
        break
    except Exception as e:
        pass

if not connected:
    print("Error: Could not connect to any Pi host.")
    sys.exit(1)

# 1. Compare ESPHome firmwares
firmwares = [
    ("/opt/esphome/config/esp32-nodo-ambiente.yaml", "lst:code_nodo_ambiente"),
    ("/opt/esphome/config/esp32-zona-escritorio.yaml", "lst:code_nodo_escritorio"),
    ("/opt/esphome/config/esp32-zona-puerta.yaml", "lst:code_nodo_puerta")
]

for pi_path, label in firmwares:
    stdin, stdout, stderr = ssh.exec_command(f"cat '{pi_path}'")
    pi_code = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    
    if err or not pi_code:
        alt_path = pi_path.replace("/opt/", f"/home/{username}/")
        stdin, stdout, stderr = ssh.exec_command(f"cat '{alt_path}'")
        pi_code = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        if not err and pi_code:
            pi_path = alt_path
            
    if not pi_code:
        print(f"Could not read {pi_path} on Pi.")
        continue
        
    print(f"\n--- Checking ESPHome Firmware: {pi_path} ---")
    latex_code = get_latex_listing(label)
    if not latex_code:
        print(f"Could not find LaTeX listing {label}.")
        continue
    
    # Normalize credentials for comparison
    pi_code_norm = re.sub(r"ssid:\s*['\"].*?['\"]", "ssid: 'nombre_red_wifi'", pi_code)
    pi_code_norm = re.sub(r"password:\s*['\"].*?['\"]", "password: 'contrasena_wifi'", pi_code_norm)
    
    pi_lines = get_clean_lines(pi_code_norm)
    latex_lines = get_clean_lines(latex_code)
    
    if pi_lines == latex_lines:
        print("MATCH! (ESPHome configuration is semantically identical).")
    else:
        print("DIFFERENCE DETECTED in ESPHome configuration:")
        diff = difflib.unified_diff(latex_lines, pi_lines, fromfile='LaTeX', tofile='Pi (Normalized)', lineterm='')
        print("\n".join(list(diff)))

# 2. Compare Home Assistant automations
ha_paths = [
    "/home/jpmorenito/homeassistant/automations.yaml",
    "/home/jpmorenito/homeassistant/config/automations.yaml"
]

ha_code = ""
active_ha_path = ""
for ha_path in ha_paths:
    stdin, stdout, stderr = ssh.exec_command(f"cat '{ha_path}'")
    code = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if not err and code:
        ha_code = code
        active_ha_path = ha_path
        break

if not ha_code:
    print("Could not read automations.yaml on Pi.")
else:
    print(f"\n--- Checking Home Assistant Automations: {active_ha_path} ---")
    
    # Parse Pi automations by splitting on "- id:"
    pi_blocks = []
    raw_blocks = re.split(r'\n-\s*id:', ha_code)
    for idx, b in enumerate(raw_blocks):
        b_full = "- id:" + b if idx > 0 or b.startswith("- id:") else b
        b_full = b_full.strip()
        if b_full:
            pi_blocks.append(b_full)
            
    # LaTeX automation labels
    labels = [
        ("lst:auto_climatizacion", "Termostato Inteligente: Modo Estudio"),
        ("lst:auto_bienestar_resumen", "Analista Local: Resumen Diario de Bienestar"),
        ("lst:auto_detect_estudio", "Contexto: Detección de Estudio (Radar Espacial)"),
        ("lst:auto_detect_sueno", "Contexto: Detección de Sueño (Fusión Radar + LDR)"),
        ("lst:auto_seguridad_alarma", "Seguridad: Alarma por Radar (Modo Manual)"),
        ("lst:auto_procrastinacion_sueno", "Bienestar: Alerta Anti-Procrastinación de Sueño"),
        ("lst:auto_ergonomia_iluminacion", "Bienestar: Iluminación Ergonomía Activa"),
        ("lst:auto_pomodoro", "Bienestar: Break Dinámico (Pomodoro)"),
        ("lst:auto_ausencia", "Contexto: Ausencia Automática por Inactividad"),
        ("lst:auto_retorno", "Contexto: Vuelta a la Habitación")
    ]
    
    for label, name in labels:
        print(f"\nVerifying: \"{name}\" ({label})")
        latex_code = get_latex_listing(label)
        if not latex_code:
            print(f"   Error: Could not find listing {label} in LaTeX.")
            continue
            
        # Extract alias from LaTeX block
        alias_match = re.search(r"alias:\s*['\"](.*?)['\"]", latex_code)
        if not alias_match:
            print(f"   Warning: Could not find alias in LaTeX listing {label}.")
            continue
        
        latex_alias = alias_match.group(1)
        norm_latex_alias = normalize_alias(latex_alias)
        
        # Find matching block on Pi
        matching_pi_block = None
        for block in pi_blocks:
            pi_alias_match = re.search(r"alias:\s*['\"](.*?)['\"]", block)
            if not pi_alias_match:
                # Try unquoted or double quoted
                pi_alias_match = re.search(r"alias:\s*(.*?)\n", block)
            
            if pi_alias_match:
                pi_alias = pi_alias_match.group(1).strip("'\"")
                if normalize_alias(pi_alias) == norm_latex_alias:
                    matching_pi_block = block
                    break
                    
        if not matching_pi_block:
            print(f"   STATUS: NOT FOUND on Pi (searched alias: \"{latex_alias}\")")
            continue
            
        # Perform line-by-line comparison
        pi_lines = get_clean_lines(matching_pi_block)
        latex_lines = get_clean_lines(latex_code)
        
        if pi_lines == latex_lines:
            print("   STATUS: MATCH (Logical equivalence verified).")
        else:
            print("   STATUS: DIFFERENCE DETECTED!")
            diff = difflib.unified_diff(latex_lines, pi_lines, fromfile='LaTeX (Clean)', tofile='Pi (Clean)', lineterm='')
            print("\n".join(list(diff)))

ssh.close()
