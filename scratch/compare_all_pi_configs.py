import sys
import paramiko
import re
import difflib

# LaTeX file paths
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
        # Remove any leading bracket artifact if the regex failed to strip it fully
        text = content_match.group(1).strip()
        if text.startswith(']'):
            text = text[1:].strip()
        return text
    return None

# Connect to Pi
hosts = ["100.70.173.44", "192.168.1.100", "192.168.1.77", "192.168.1.200", "jacob-pi"]
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

# Compare ESPHome firmwares
firmwares = [
    ("/opt/esphome/config/esp32-nodo-ambiente.yaml", "lst:code_nodo_ambiente"),
    ("/opt/esphome/config/esp32-zona-escritorio.yaml", "lst:code_nodo_escritorio"),
    ("/opt/esphome/config/esp32-zona-puerta.yaml", "lst:code_nodo_puerta")
]

for pi_path, label in firmwares:
    # Try alternate path if /opt/esphome doesn't work
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
    
    # Normalize credentials for comparison
    # Replace real credentials on Pi with placeholders for comparison
    pi_code_norm = re.sub(r"ssid:\s*['\"].*?['\"]", "ssid: 'nombre_red_wifi'", pi_code)
    pi_code_norm = re.sub(r"password:\s*['\"].*?['\"]", "password: 'contrasena_wifi'", pi_code_norm)
    
    pi_lines = [line.strip() for line in pi_code_norm.splitlines() if line.strip()]
    latex_lines = [line.strip() for line in latex_code.splitlines() if line.strip()]
    
    if pi_lines == latex_lines:
        print("MATCH! (ESPHome configuration is 100% identical).")
    else:
        print("DIFFERENCE DETECTED in ESPHome configuration:")
        diff = difflib.unified_diff(latex_lines, pi_lines, fromfile='LaTeX', tofile='Pi (Normalized)', lineterm='')
        print("\n".join(list(diff)[:15]))

# Compare Home Assistant automations
# Let's read the Pi's automations.yaml
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
    # In LaTeX, we have 10 separate listings:
    labels = [
        "lst:auto_climatizacion",
        "lst:auto_bienestar_resumen",
        "lst:auto_detect_estudio",
        "lst:auto_detect_sueno",
        "lst:auto_seguridad_alarma",
        "lst:auto_procrastinacion_sueno",
        "lst:auto_ergonomia_iluminacion",
        "lst:auto_pomodoro",
        "lst:auto_ausencia",
        "lst:auto_retorno"
    ]
    
    # Let's parse each listing from LaTeX
    for label in labels:
        latex_code = get_latex_listing(label)
        if not latex_code:
            print(f"Warning: could not find listing {label} in LaTeX.")
            continue
            
        # Try to find this automation in the Pi's automations.yaml by checking if the alias exists
        # In LaTeX, each block has: alias: '...' or similar.
        alias_match = re.search(r"alias:\s*['\"](.*?)['\"]", latex_code)
        if not alias_match:
            print(f"Warning: could not find alias in listing {label}.")
            continue
            
        alias = alias_match.group(1)
        print(f"Verifying automation alias: \"{alias}\"")
        
        # Let's verify if the alias exists in the Pi's file
        # We can do a simple check to see if the block of LaTeX is a subset of the Pi's code,
        # or we can extract the corresponding block from the Pi's file.
        # An easy way to compare is: is the alias in the Pi's code?
        if alias in ha_code:
            print("   Status: FOUND on Raspberry Pi.")
        else:
            print(f"   Status: NOT FOUND on Raspberry Pi (alias: \"{alias}\")")

ssh.close()
