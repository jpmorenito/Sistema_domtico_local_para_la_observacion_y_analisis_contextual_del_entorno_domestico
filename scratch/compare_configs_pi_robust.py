import sys
import paramiko
import re
import difflib

# LaTeX file paths
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

# Try connecting to Raspberry Pi
hosts = ["100.70.173.44", "192.168.1.200", "192.168.1.100", "192.168.137.111", "jacob-pi"]
username = "jpmorenito"
password = "jpmorenito"

connected = False
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for host in hosts:
    try:
        print(f"Trying to connect to {host}...")
        ssh.connect(host, username=username, password=password, timeout=3)
        print(f"Connected successfully to {host}!")
        connected = True
        break
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")

if not connected:
    print("Error: Could not connect to any Raspberry Pi host.")
    sys.exit(1)

# Files to check on Pi and their corresponding labels in LaTeX
# We check both /opt/esphome/config and /home/jpmorenito/esphome/config
# and /home/jpmorenito/homeassistant/config/automations.yaml or /home/jpmorenito/homeassistant/automations.yaml
paths_to_try = [
    # (pi_path, latex_label)
    ("/opt/esphome/config/esp32-nodo-ambiente.yaml", "lst:code_nodo_ambiente"),
    ("/home/jpmorenito/esphome/config/esp32-nodo-ambiente.yaml", "lst:code_nodo_ambiente"),
    
    ("/opt/esphome/config/esp32-zona-escritorio.yaml", "lst:code_nodo_escritorio"),
    ("/home/jpmorenito/esphome/config/esp32-zona-escritorio.yaml", "lst:code_nodo_escritorio"),
    
    ("/opt/esphome/config/esp32-zona-puerta.yaml", "lst:code_nodo_puerta"),
    ("/home/jpmorenito/esphome/config/esp32-zona-puerta.yaml", "lst:code_nodo_puerta"),
    
    ("/home/jpmorenito/homeassistant/automations.yaml", "lst:code_ha_automaciones"),
    ("/home/jpmorenito/homeassistant/config/automations.yaml", "lst:code_ha_automaciones")
]

checked_labels = set()

for pi_path, label in paths_to_try:
    if label in checked_labels:
        continue
        
    # Read file from Pi
    stdin, stdout, stderr = ssh.exec_command(f"cat '{pi_path}'")
    pi_code = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    
    if err or not pi_code:
        # Try next alternative path
        continue
        
    print(f"\n==================================================")
    print(f"Comparing {pi_path} with LaTeX listing: {label}")
    print(f"==================================================")
    checked_labels.add(label)
            
    # Read listing from LaTeX
    latex_code = get_latex_listing(label)
    if not latex_code:
        print(f"Could not find listing with label {label} in LaTeX file.")
        continue
        
    # Clean up codes for comparison (normalize whitespace, line endings)
    pi_lines = [line.strip() for line in pi_code.splitlines() if line.strip()]
    latex_lines = [line.strip() for line in latex_code.splitlines() if line.strip()]
    
    # Compare
    if pi_lines == latex_lines:
        print("MATCH! The code in the document matches the active code on the Pi.")
    else:
        print("DIFFERENCE DETECTED!")
        # Print diff
        diff = difflib.unified_diff(
            latex_lines, 
            pi_lines, 
            fromfile='LaTeX Document', 
            tofile=f'Pi ({pi_path})', 
            lineterm=''
        )
        print("\n".join(list(diff)[:30])) # Show first 30 lines of diff
        if len(list(diff)) > 30:
            print("...")

ssh.close()
