import sys
import paramiko
import re
import difflib

# LaTeX file paths
latex_file = "c:/Users/jacob/Downloads/TFG/Documento final/B_manual_tecnico_codigo.tex"

# SSH connection details
host = "100.70.173.44"
username = "jpmorenito"
password = "jpmorenito"

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

# Connect to Raspberry Pi
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to {host}...")
    ssh.connect(host, username=username, password=password, timeout=5)
    print("Connected successfully!")
except Exception as e:
    print(f"Error connecting: {e}")
    sys.exit(1)

# Files to check on Pi and their corresponding labels in LaTeX
files_to_check = {
    "/opt/esphome/config/esp32-nodo-ambiente.yaml": "lst:code_nodo_ambiente",
    "/opt/esphome/config/esp32-zona-escritorio.yaml": "lst:code_nodo_escritorio",
    "/opt/esphome/config/esp32-zona-puerta.yaml": "lst:code_nodo_puerta",
    "/home/jpmorenito/homeassistant/automations.yaml": "lst:code_ha_automaciones" # Let's verify this label
}

# Wait, let's find the labels in LaTeX for all listings
# Let's search B_manual_tecnico_codigo.tex for listings and their labels
listings = re.findall(r'\\begin\{lstlisting\}[^\]]*label=\{(.*?)\}', latex_content)
print(f"Found listings with labels in LaTeX: {listings}")

for pi_path, label in files_to_check.items():
    print(f"\n==================================================")
    print(f"Checking {pi_path} (LaTeX label: {label})")
    print(f"==================================================")
    
    # Read file from Pi
    stdin, stdout, stderr = ssh.exec_command(f"cat '{pi_path}'")
    pi_code = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if err:
        print(f"Error reading file from Pi: {err}")
        # Try checking different path for automations if it failed
        if "automations.yaml" in pi_path:
            alt_path = "/home/jpmorenito/homeassistant/config/automations.yaml"
            print(f"Trying alternative path: {alt_path}")
            stdin, stdout, stderr = ssh.exec_command(f"cat '{alt_path}'")
            pi_code = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if err:
                print(f"Alt path failed: {err}")
                continue
            else:
                pi_path = alt_path
        else:
            continue
            
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
        print("MATCH! The code in the document matches the code on the Pi.")
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
        print("...")

ssh.close()
