import paramiko
import re

# SSH Connection settings
host = "100.70.173.44"
username = "jpmorenito"
password = "jpmorenito"
pi_path = "/home/jpmorenito/homeassistant/automations.yaml"
temp_path = "/home/jpmorenito/automations_temp.yaml"

# Connect via SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print(f"Connecting to {host}...")
ssh.connect(host, username=username, password=password)
print("Connected!")

# Read the file
s_in, s_out, s_err = ssh.exec_command(f"cat '{pi_path}'")
content = s_out.read().decode("utf-8")
err = s_err.read().decode("utf-8")

if err:
    print(f"Error reading file: {err}")
    ssh.close()
    exit(1)

# Let's perform a precise replacement of the message block within the 'informe_diario_qol' automation.
blocks = content.split("\n- ")
modified = False

for i, block in enumerate(blocks):
    # Determine if this is the block we want
    if "id: informe_diario_qol" in block or "id: 'informe_diario_qol'" in block:
        print("Found target wellness summary automation block.")
        new_block = block
        
        # Replace tiempo_de_estudio
        if "sensor.tiempo_de_estudio" in new_block and "sensor.tiempo_de_estudio') | float(0) | round(2)" not in new_block:
            new_block = re.sub(
                r"states\(\s*['\"]sensor\.tiempo_de_estudio['\"]\s*\)",
                "states('sensor.tiempo_de_estudio') | float(0) | round(2)",
                new_block
            )
        
        # Replace tiempo_de_sueno
        if "sensor.tiempo_de_sueno" in new_block and "sensor.tiempo_de_sueno') | float(0) | round(2)" not in new_block:
            new_block = re.sub(
                r"states\(\s*['\"]sensor\.tiempo_de_sueno['\"]\s*\)",
                "states('sensor.tiempo_de_sueno') | float(0) | round(2)",
                new_block
            )
            
        if new_block != block:
            blocks[i] = new_block
            modified = True
            print("Successfully updated the wellness summary template in python script memory.")
        else:
            print("No modification needed or already modified.")

if modified:
    new_content = "\n- ".join(blocks)
    
    # Upload to temp path
    print("Uploading modified file to temp path...")
    sftp = ssh.open_sftp()
    with sftp.file(temp_path, "w") as f:
        f.write(new_content)
    sftp.close()
    
    # Move to destination using sudo
    print("Moving temp file to automations.yaml using sudo...")
    cmd = f"echo '{password}' | sudo -S cp '{temp_path}' '{pi_path}'"
    s_in, s_out, s_err = ssh.exec_command(cmd)
    
    # Wait for the command to finish
    out_msg = s_out.read().decode("utf-8")
    err_msg = s_err.read().decode("utf-8")
    
    # Clean up temp file
    ssh.exec_command(f"rm '{temp_path}'")
    
    print(f"Sudo output: {out_msg}")
    print(f"Sudo error: {err_msg}")
    print("Done! File successfully updated on Pi.")
else:
    print("No changes were made.")

ssh.close()
