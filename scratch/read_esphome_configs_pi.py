import sys
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

host = "100.70.173.44"
username = "jpmorenito"
password = "jpmorenito"

try:
    print(f"Connecting to {host}...")
    ssh.connect(host, username=username, password=password, timeout=5)
    print("Connected successfully!")
except Exception as e:
    print(f"Error connecting: {e}")
    sys.exit(1)

# List files in /opt/esphome/config
print("Files in /opt/esphome/config:")
stdin, stdout, stderr = ssh.exec_command("ls -la /opt/esphome/config")
print(stdout.read().decode())

# Read any .yaml or .yml files found in /opt/esphome/config
print("Finding all YAML files in /opt/esphome/config:")
stdin, stdout, stderr = ssh.exec_command("find /opt/esphome/config -name '*.yaml' -o -name '*.yml'")
yaml_files = stdout.read().decode().strip().split("\n")

for yf in yaml_files:
    if yf:
        print(f"\n==================================================")
        print(f"File: {yf}")
        print(f"==================================================")
        stdin, stdout, stderr = ssh.exec_command(f"cat '{yf}'")
        print(stdout.read().decode())

ssh.close()
