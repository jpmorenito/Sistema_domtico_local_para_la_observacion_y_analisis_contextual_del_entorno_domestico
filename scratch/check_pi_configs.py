import sys
import os

try:
    import paramiko
except ImportError:
    print("paramiko not installed. Installing it first via subprocess...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

hosts = ["100.70.173.44", "192.168.1.200", "192.168.137.111", "jacob-pi"]
username = "jpmorenito"
password = "jpmorenito"

connected = False
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for host in hosts:
    try:
        print(f"Trying to connect to {host}...")
        ssh.connect(host, username=username, password=password, timeout=5)
        print(f"Successfully connected to {host}!")
        connected = True
        break
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")

if not connected:
    print("Could not connect to any Raspberry Pi hosts. Exiting.")
    sys.exit(1)

# List esphome configuration directory
print("Listing files in /home/jpmorenito/esphome/config:")
stdin, stdout, stderr = ssh.exec_command("ls -la /home/jpmorenito/esphome/config")
print(stdout.read().decode())

# Read all yaml files
files_to_read = [
    "esp32-nodo-ambiente.yaml",
    "esp32-zona-escritorio.yaml",
    "esp32-zona-puerta.yaml",
    "esp32-nodo-ambiente.yml",
    "esp32-zona-escritorio.yml",
    "esp32-zona-puerta.yml"
]

for f in files_to_read:
    print(f"Checking for /home/jpmorenito/esphome/config/{f}...")
    stdin, stdout, stderr = ssh.exec_command(f"cat /home/jpmorenito/esphome/config/{f}")
    content = stdout.read().decode()
    err = stderr.read().decode()
    if content:
        print(f"--- CONTENT OF {f} ---")
        print(content)
        print("-----------------------")
    elif err:
        # File probably does not exist or empty
        pass

ssh.close()
