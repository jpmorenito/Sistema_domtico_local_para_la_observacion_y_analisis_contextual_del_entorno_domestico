import sys
import paramiko

host = "192.168.1.77"
username = "jpmorenito"
password = "jpmorenito"

new_ssid = "Livebox6s-4ADB_EXT"
new_pass = "PjEM5okD45N4"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to Raspberry Pi at {host}...")
    ssh.connect(host, username=username, password=password, timeout=5)
    print("Connected successfully!\n")
except Exception as e:
    print(f"Error connecting: {e}")
    sys.exit(1)

# Helper to read file from Pi
def cat_file(path):
    stdin, stdout, stderr = ssh.exec_command(f"cat '{path}'")
    return stdout.read().decode()

# Helper to write file to Pi
def write_file(path, content):
    # We write via a temporary file on the Pi to avoid permission issues
    tmp_path = "/tmp/esphome_tmp"
    stdin, stdout, stderr = ssh.exec_command(f"cat > '{tmp_path}'")
    stdin.write(content)
    stdin.close()
    stdout.read() # Wait for execution
    
    # Copy to destination using sudo
    cmd = f"echo {password} | sudo -S cp '{tmp_path}' '{path}' && rm '{tmp_path}'"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read() # Wait for execution

# 1. Update secrets.yaml
print("Updating secrets.yaml...")
new_secrets = f"""# Your Wi-Fi SSID and password
wifi_ssid: "{new_ssid}"
wifi_password: "{new_pass}"
"""
write_file("/opt/esphome/config/secrets.yaml", new_secrets)

# 2. Update esp32-nodo-ambiente.yaml
print("Updating esp32-nodo-ambiente.yaml...")
content = cat_file("/opt/esphome/config/esp32-nodo-ambiente.yaml")
# Replace wifi
content = content.replace("ssid: 'Livebox6s-479B'", f"ssid: '{new_ssid}'")
content = content.replace("password: 'jjCLnhaS56aA'", f"password: '{new_pass}'")
write_file("/opt/esphome/config/esp32-nodo-ambiente.yaml", content)

# 3. Update esp32-zona-escritorio.yaml
print("Updating esp32-zona-escritorio.yaml...")
content = cat_file("/opt/esphome/config/esp32-zona-escritorio.yaml")
# Replace wifi
content = content.replace("ssid: 'Livebox6s-479B'", f"ssid: '{new_ssid}'")
content = content.replace("password: 'jjCLnhaS56aA'", f"password: '{new_pass}'")
# Also handle double quotes in some files
content = content.replace('ssid: "Livebox6s-479B"', f'ssid: "{new_ssid}"')
content = content.replace('password: "jjCLnhaS56aA"', f'password: "{new_pass}"')
write_file("/opt/esphome/config/esp32-zona-escritorio.yaml", content)

# 4. Update esp32-zona-puerta.yaml (and add Laser Switch)
print("Updating esp32-zona-puerta.yaml...")
content = cat_file("/opt/esphome/config/esp32-zona-puerta.yaml")
content = content.replace("ssid: 'Livebox6s-479B'", f"ssid: '{new_ssid}'")
content = content.replace("password: 'jjCLnhaS56aA'", f"password: '{new_pass}'")
content = content.replace('ssid: "Livebox6s-479B"', f'ssid: "{new_ssid}"')
content = content.replace('password: "jjCLnhaS56aA"', f'password: "{new_pass}"')

# Add laser switch if not already present
if "laser_puerta" not in content:
    print("Adding missing laser switch to esp32-zona-puerta.yaml...")
    laser_block = """
# 2. EMISOR LASER (BARRERA/ALARMA)
switch:
  - platform: gpio
    pin: 5
    name: 'Laser Puerta'
    id: laser_puerta
    restore_mode: ALWAYS_OFF
"""
    # Find last line or just append
    content = content.rstrip() + "\n" + laser_block
write_file("/opt/esphome/config/esp32-zona-puerta.yaml", content)

# 5. Move duplicate file to archive
print("Archiving duplicate puerta factory file...")
cmd = f"echo {password} | sudo -S mv /opt/esphome/config/esp32-zona-puertafactorybin.yaml /opt/esphome/config/archive/esp32-zona-puertafactorybin.yaml"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read() # Wait for execution

print("\nAll ESPHome configurations updated successfully on the Pi!")
ssh.close()
